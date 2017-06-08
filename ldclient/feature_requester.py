from __future__ import absolute_import

import requests
from cachecontrol import CacheControl

from ldclient.interfaces import FeatureRequester
from ldclient.util import _headers
from ldclient.util import log


class FeatureRequesterImpl(FeatureRequester):
    def __init__(self, config):
        self._session = CacheControl(requests.Session())
        self._config = config

    def get_all(self):
        hdrs = _headers(self._config.sdk_key)
        uri = self._config.get_latest_flags_uri
        r = self._session.get(uri, headers=hdrs,
                              timeout=(self._config.connect_timeout,
                                       self._config.read_timeout))
        r.raise_for_status()
        flags = r.json()
        versions_summary = list(map(lambda f: "{0}:{1}".format(f.get("key"), f.get("version")), flags.values()))
        log.debug("Get All flags response status:[{0}] From cache?[{1}] ETag:[{2}] flag versions: {3}"
                  .format(r.status_code, r.from_cache, r.headers.get('ETag'), versions_summary))
        return flags

    def get_one(self, key):
        #TODO: Do we ever want to cache this response?
        hdrs = _headers(self._config.sdk_key)
        uri = self._config.get_latest_flags_uri + '/' + key
        log.debug("Getting one feature flag using uri: " + uri)
        r = self._session.get(uri,
                              headers=hdrs,
                              timeout=(self._config.connect_timeout,
                                       self._config.read_timeout))
        r.raise_for_status()
        flag = r.json()
        log.debug("Get one flag response status:[{0}] From cache?[{1}] Flag key:[{2}] version:[{3}]"
                  .format(r.status_code, r.from_cache, key, flag.get("version")))
        return flag
