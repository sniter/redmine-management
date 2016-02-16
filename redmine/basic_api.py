# -*- coding: utf-8 -*-
__author__ = 'Ilya Babich <i.babich@invento.by>'

import urllib
import urllib2
import json
import ssl
import re
import sys


_host_slashes_re = ur'/*$'


class RedmineApi(object):

    def __init__(self, **kwargs):
        self._url = re.sub(_host_slashes_re, '', kwargs.get('host', 'http://localhost'))
        self._login = kwargs.get('login', 'admin')
        self._password = kwargs.get('password', 'admin')
        self._token = kwargs.get('token', None)
        self._project_id = kwargs.get('project_id', None)
        self._use_token = self._token is None

    def _json_call(self, url, **kwargs):
        url_params = kwargs.get('url_params', None)
        headers = kwargs.get('headers', {})
        headers.update({'X-Redmine-API-Key': self._token    })

        request = urllib2.Request(url + '?' +  urllib.urlencode(url_params))

        for header, header_value in headers.iteritems():
            request.add_header(header, header_value)

        # context = ssl._create_unverified_context()
        return json.loads(urllib2.urlopen(request).read())

    def issues(self, **kwargs):
        url = '/'.join([self._url, 'issues.json'])
        url_param_keys = ['offset', 'limit', 'sort', 'project_id', 'subproject_id', 'tracker_id', 'status_id',
                          'assigned_to_id', 'cf_x', 'created_on', 'updated_on']

        existing_url_params = filter(lambda p: kwargs.get(p, None) is not None, url_param_keys)
        url_params = dict((p, kwargs[p]) for p in existing_url_params)

        return self._json_call(url, url_params=url_params)

    def issue(self, issue_id, **kwargs):
        url = '/'.join([re.subself._url, 'issues', '%d.json' % issue_id])
        url_param_keys = ['include']

        existing_url_params = filter(lambda p: kwargs.get(p, None) is not None, url_param_keys)
        url_params = urllib.urlencode(dict((p, kwargs[p]) for p in existing_url_params))

        return self._json_call(url, url_params=url_params)
