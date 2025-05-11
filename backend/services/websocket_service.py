from chessArena.chess_engine import ChessEngine
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
import websockets
from json import loads, dumps

# class WebSocketService:
#     def __init__(self, move_queue, game_request_queue):
#         self.move_queue = move_queue
#         self.game_request_queue = game_request_queue
    
#     async def handle_connection(self, websocket):
#         print('*'*50)
#         print('IN HANDLE_CONNECTIONS FUNC')
#         print(websocket)
#         print('*'*50)
#         try:
#             while True:
#                 message = await websocket.recv()
                
#                 data = loads(message)
                
#                 game_information_dto = await self.handle_message(data)
                
#                 print(game_information_dto, ' - type: ', type(game_information_dto))
                
#                 test = await websocket.send(dumps(game_information_dto))
#                 print(test)
                
#         except websockets.exceptions.ConnectionClosed:
#             print('client disconnected')
            
#     async def handle_message(self, response):
#         print('<>'*50)
#         print('MESSAGE RECEIVED')
#         print(response)
#         print('<>'*50)
        
#         data = loads(response['data'])
                        
#         # TODO - will need to expand this out to handle termination and restart
#         match data.get('type'):
#             case 'new_game':
#                 await self.game_request_queue.put(data)
#                 print('new game - added to queue')
#             case 'new_move':
#                 await self.move_queue.put(data)
#                 print('new move - added to queue')
                        
#         # TODO - will need to change if two players are both manual
#         # this is expectin the computer to make a response
#         move = await self.move_queue.get()
        
#         return move

#     async def start_server(self):
#         print('listening on port 5000')
#         async with websockets.serve(self.handle_connection, '0.0.0.0', 5000):
#             await asyncio.Event().wait()


# REQUIREMENTS:
# 1. Need to wait on a message coming in - which has a game request
# 2. Needs to also keep the connection alive constantly incase a terminate-game or restart-game request come through
# once a game has been loaded...
# 1. Need to be waiting on messages coming in over the websocket connection - it could be manual vs manual
# 2. Need to constantly keep polling for new messages coming in from the move_queue - could select to agents to play each other
# 

class WebSocketService:
    def __init__(self, game_request_queue: asyncio.Queue = None, incoming_move_queue: asyncio.Queue = None,
                 outgoing_move_queue: asyncio.Queue = None, results_queue: asyncio.Queue = None):
        # set Queues
        self.game_request_queue = game_request_queue
        self.incoming_move_queue = incoming_move_queue
        self.outgoing_move_queue = outgoing_move_queue
        self.results_queue = results_queue
        
    async def start_server(self):
        async with websockets.serve(self.handle_connection, '0.0.0.0', 5000):
            await asyncio.Future()
            
    async def handle_connection(self, websocket):
        print("new client connected")
        
        async def receive_from_client():
            try:
                async for message in websocket:
                    await self.handle_client_message(message)
            except websockets.exceptions.ConnectionClosed:
                print('client disconnected - error in handle_connection func')
                
        async def poll_game_requests():
            while True:
                game_request = await self.game_request_queue.get()
                print('*'*50)
                print(game_request)
                print('*'*50)
                
        async def send_moves_to_client():
            print('YOYOYOYOYOYOYO')
            while True:
                print('We about to wait on move queue')
                move = await self.outgoing_move_queue.get()
                print('6'*50)
                print('HOLY FUCKBALLS CHICKEN AND CHIPS', move)
                print('6'*50)
                await websocket.send(dumps(move))
                print('send move to client', move)
                
        await asyncio.gather(
            receive_from_client(),
            send_moves_to_client(),
            poll_game_requests(),
        )
                
    async def handle_client_message(self, raw_message):
        print('Received raw message:', raw_message, type(raw_message))
        try: 
            msg = loads(raw_message)
            data = loads(msg["data"])
            match data.get('type'):
                case "new_game":
                    await self.game_request_queue.put(data)
                case "new_move":
                    print('ADDING TO MOVE QUEUE - TYPE:', type(data))
                    print(data)
                    await self.incoming_move_queue.put(data)
                case _:
                    print('unknown message type:', data)
        except Exception as e:
            print("error handling client message:", e)
        