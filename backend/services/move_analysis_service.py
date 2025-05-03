from logger.logger_config import Logging

loggingConfig = Logging()
logger = loggingConfig.get_logger('moveAnalysis')

class MoveAnalysisService:
    '''
    Runs stockfish engine to analyse the best move for a given board + rate the move made by the agent (coming in through the other process)
    - Would i need some sort of queue to handle the requests if they are coming in locally and asynchronously?
    '''
    
    def __init__(self, connect_web_sockets):
        if connect_web_sockets:
            logger.info('analysing move with websocket')
            # implement websockets
            ...
        else:
            logger.info('analysing move without websocket')
            ...