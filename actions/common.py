__author__ = 'ilya'

import console
import textwrap
from termcolor import colored
from redmine.resources import Tracker
from redmine.resources import User
from redmine.resources import Issue
from redmine.resources import IssueStatus
from redmine.resources import IssueJournal
from redmine.resources import TimeEntry

_classes = [Tracker, User, Issue, IssueStatus, IssueJournal, TimeEntry]


def _res_to_dict(record, fields=None):
    if fields is None:
        fields = dir(record)

    result = {}

    for field in fields:
        value = record[field]
        for clazz in _classes:
            if isinstance(value, clazz):
                result[field] = _res_to_dict(value)
            else:
                result[field] = field

    return result


class CommonRender(object):

    def __init__(self):
        (self.monitor_width, self.monitor_height) = console.getTerminalSize()
        self.twrapper = textwrap.TextWrapper(width=self.monitor_width, replace_whitespace=False, drop_whitespace=False)

    def _decorate_priority(self, priority):
        v = '%s' % priority
        res = u'%10s' % priority
        if v == 'Immediate':
            return colored(res, 'red', attrs=['bold'])
        if v == 'Urgent':
            return colored(res, 'red')
        if v == 'High':
            return colored(res, 'yellow')

        return colored(res, 'green')

    def _decorate_done(self, value):
        v = int(value)
        res = u'%3s%%' % value
        if v == 0:
            return colored(res, 'red', attrs=['bold'])
        if v <= 50:
            return colored(res, 'yellow', attrs=['bold'])
        if v < 100:
            return colored(res, 'yellow')

        return colored(res, 'green')

    def _decorate_status(self, value):
        v = u'%s' % value
        res = u'%12s' % value
        if v == 'New':
            return colored(res, 'red')
        if v == 'In Progress':
            return colored(res, 'yellow')
        if v == 'Feedback':
            return colored(res, 'red', attrs=['bold'])
        if v == 'Closed':
            return colored(res, 'grey')

        return colored(res, 'green')

    def _decorate_id(self, value):
        return colored(value, 'white', attrs=['bold'])
