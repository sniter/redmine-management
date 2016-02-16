__author__ = 'ilya'

from termcolor import colored
from common import CommonRender
import pprint
import sys

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


class TaskList(CommonRender):

    def __call__(self, **kwargs):
        connection = kwargs.get('connection', None)
        args = kwargs.get('args', None)
        _pp = MyPrettyPrinter(indent=2)
        issues = connection.issues(project_id=args.project, assigned_to_id='me', limit=args.limit, sort=args.sort)

        for issue in issues['issues']:

            # print(issue)

            print u' '.join(map(lambda v: u'%s' % v, [
                self._decorate_id(issue['id']),
                self._decorate_status(issue.get('status', {}).get('name', None)),
                self._decorate_priority(issue.get('priority', {}).get('name', None)),
                self._decorate_done(issue['done_ratio']),
                colored(issue['subject'], 'white')
            ]))
            descr = None  # u'%{description}'.format(**dict_issue)

            # for line in twrapper.wrap(subj):
            #     print colored(unicode(line), 'green')
            if descr:
                print colored('-' * self.monitor_width, 'green')
                for line in self.twrapper.wrap(descr):
                    print colored(line, 'white')
