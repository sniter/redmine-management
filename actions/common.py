from collections import Sequence

__author__ = 'ilya'

import console
import textwrap
from termcolor import colored
# from redmine.resources import Tracker
# from redmine.resources import User
# from redmine.resources import Issue
# from redmine.resources import IssueStatus
# from redmine.resources import IssueJournal
# from redmine.resources import TimeEntry
# from redmine.resultsets import ResourceSet

# _classes = [Tracker, User, Issue, IssueStatus, IssueJournal, TimeEntry]


def _res_to_dict(record, fields=None):
    if fields is None:
        fields = dir(record)

    result = {}

    for field in fields:
        value = record[field]
        # for clazz in _classes:
        #     if isinstance(value, clazz):
        #         result[field] = _res_to_dict(value)
        #     # elif isinstance(value, ResourceSet):
        #     #     result[field] = value.values('hours', 'spent_on', 'comments', 'activity_id')
        #     else:
        #         result[field] = value

    return result


class CommonRender(object):

    def __init__(self):
        (self.monitor_width, self.monitor_height) = console.getTerminalSize()
        self.twrapper = textwrap.TextWrapper(width=self.monitor_width, replace_whitespace=False, drop_whitespace=False)
        self.priority_tpl = u'%10s'
        self.done_tpl = u'%3s%%'
        self.status_tpl = u'%12s'

    def _decorate_priority(self, priority):
        v = u'%s' % priority
        res = self.priority_tpl % priority
        if v == 'Immediate':
            return colored(res, 'red', attrs=['bold'])
        if v == 'Urgent':
            return colored(res, 'red')
        if v == 'High':
            return colored(res, 'yellow')

        return colored(res, 'green')

    def _decorate_done(self, value):
        v = int(value)
        res = self.done_tpl % value
        if v == 0:
            return colored(res, 'red', attrs=['bold'])
        if v <= 50:
            return colored(res, 'yellow', attrs=['bold'])
        if v < 100:
            return colored(res, 'yellow')

        return colored(res, 'green')

    def _decorate_status(self, value):
        v = u'%s' % value
        res = self.status_tpl % value
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

    def _decorate_subject(self, subject):
        return colored(subject, 'white')
