import sys
sys.dont_write_bytecode = True

import argparse
from thread_handler import ThreadHandler
import asyncio

parser = argparse.ArgumentParser(description="Chess Engine with Command-Line Arguments")
parser.add_argument('-web', action='store_true', help="Enable web app")

async def main():
    
    args = parser.parse_args()
    thread_handler = ThreadHandler()
    
    if args.web:
        await thread_handler.run_dual_threads()
    else:
        default_params = {
            'selected_player_names': ['RandomAgent', 'RandomAgent'],
            'starts': 'P1',
            'game_length': '5min',
        }
        thread_handler.run_game_no_threads(default_params)
    
if __name__ == '__main__':
    asyncio.run(main())