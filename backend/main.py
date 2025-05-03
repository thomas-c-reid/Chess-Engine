import sys

sys.dont_write_bytecode = True

import signal
import argparse
from process_handler import ProcessHandler

def main():
    parser = argparse.ArgumentParser(description="Chess Engine for RL agents")
    parser.add_argument('-web', action='store_true', help="Enable web app")
    
    args = parser.parse_args()
    
    process_handler = ProcessHandler(connect_web_sockets=args.web)
    
    # Listen for Ctrl+C (KeyboardInterrupt) to terminate gracefully
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C

    try:
        # Keep the program running until Ctrl+C is pressed
        while True:
            pass
    except KeyboardInterrupt:
        # This block is optional since the signal_handler handles the exit
        print("Program terminated.")
        process_handler.terminate()  # Ensure the processes are terminated if needed
        sys.exit(0)
    
def signal_handler(sig, frame):
    print("Ctrl+C caught. Shutting down the game...")
    sys.exit(0)
        
if __name__ == '__main__':
    main()