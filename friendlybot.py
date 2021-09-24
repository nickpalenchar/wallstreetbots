import requests
import logging
from time import sleep
from datetime import datetime, timedelta

log = logging.getLogger(__name__)

class FriendlyBot:


    def __init__(self, speed_limit=2):
        self.speed_limit = speed_limit
        self._last_request = datetime(1979, 1, 1)


    def request(self, *args, wait_for_greenlight=True, **kwargs):

        if wait_for_greenlight:
            self.wait_for_greenlight()

        self._last_request = datetime.now() 
        response = requests.request(*args, **kwargs)

        if response.status_code == 429:
            log.debug(f'retry-after header is {response.headers["retry-after"]}')
            wait_time = int(response.headers['retry-after'])
            log.info(f'⏳ Must wait {wait_time} seconds...')
            sleep(wait_time)
            log.info('🌐 retrying request')
            return self.request(*args, wait_for_greenlight=False, **kwargs)

        return response

    def wait_for_greenlight(self):
        """Ensures speed limit is being followed before issuing requets"""

        now = datetime.now()
        time_to_wait = timedelta(seconds=self.speed_limit) - (now - self._last_request)
        if time_to_wait > timedelta(0):
            seconds_to_wait = time_to_wait.seconds + 1
            log.info(f'sleeping {seconds_to_wait} seconds')
            sleep(seconds_to_wait)
        else:
            log.debug('wait_for_greenlight: not speeding, going to request')
