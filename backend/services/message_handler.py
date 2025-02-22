from queue import Queue

class MessageHandler:
    def __init__(self):
        self.move_queue = Queue()
        self.game_requests = []
        self.messages = []
        
    def put_message(self, message):
        self.messages.append(message)
        print(self.messages)
        
    def start_game_message(self, message):
        self.game_requests.append(message)
        print(self.game_requests)
                    
    # def get_move(self, timeout=None):
    #     self._event.wait(timeout=timeout)
    #     with self._lock:
    #         if not self.move_queue.empty():
    #             self._event.clear()
    #             return self.move_queue.get()
    #         return None