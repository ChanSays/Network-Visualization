import sys
import logging
from utils.logger import Logger

log = Logger(__name__)
log.setup_log(console_level=logging.DEBUG)


class HealthMonitor:
    def __init__(self):
        pass

    def check_health(self):
        pass

def check_health:
    # grep running process
    
    # quit if non-exist
    
    # check DB
    
    # exists:remove
    
    # exit
    
def main():
    log.info("Health Monitor cron started")
    hlth = HealthMonitor()
    hlth.check_health()
    log.info("Health Monitor cron ended")

if __name__ == "__main__":
    main()
