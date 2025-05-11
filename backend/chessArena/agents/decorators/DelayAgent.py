import datetime
from functools import wraps
import time

class DelayAgent:
    def __init__(self, delay_seconds=0.5):
        self.delay_seconds = delay_seconds
        
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            finish_time = datetime.datetime.now()
            
            execution_time = (finish_time - start_time).total_seconds()
            remaining_time = self.delay_seconds - execution_time

            if remaining_time > 0:
                time.sleep(remaining_time)            
            return result
        return wrapper