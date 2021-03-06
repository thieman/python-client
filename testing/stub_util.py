from email.utils import formatdate
from requests.structures import CaseInsensitiveDict

from ldclient.interfaces import EventProcessor, FeatureRequester, UpdateProcessor


class MockEventProcessor(EventProcessor):
    def __init__(self, *_):
        self._running = False
        self._events = []
        mock_event_processor = self

    def stop(self):
        self._running = False

    def start(self):
        self._running = True

    def is_alive(self):
        return self._running

    def send_event(self, event):
        self._events.append(event)

    def flush(self):
        pass

class MockFeatureRequester(FeatureRequester):
    def __init__(self):
        self.all_data = {}
        self.exception = None

    def get_all_data(self):
        if self.exception is not None:
            raise self.exception
        return self.all_data

    def get_one(self, kind, key):
        pass

class MockResponse(object):
    def __init__(self, status, headers):
        self._status = status
        self._headers = headers

    @property
    def status(self):
        return self._status

    def getheader(self, name):
        return self._headers.get(name.lower())

class MockHttp(object):
    def __init__(self):
        self._request_data = None
        self._request_headers = None
        self._response_status = 200
        self._server_time = None

    def request(self, method, uri, headers, timeout, body, retries):
        self._request_headers = headers
        self._request_data = body
        resp_hdr = dict()
        if self._server_time is not None:
            resp_hdr['date'] = formatdate(self._server_time / 1000, localtime=False, usegmt=True)
        return MockResponse(self._response_status, resp_hdr)

    def clear(self):
        pass

    @property
    def request_data(self):
        return self._request_data

    @property
    def request_headers(self):
        return self._request_headers

    def set_response_status(self, status):
        self._response_status = status
    
    def set_server_time(self, timestamp):
        self._server_time = timestamp

    def reset(self):
        self._request_headers = None
        self._request_data = None

class MockUpdateProcessor(UpdateProcessor):
    def __init__(self, config, store, ready):
        ready.set()

    def start(self):
        pass

    def stop(self):
        pass

    def is_alive(self):
        return True

    def initialized(self):
        return True
