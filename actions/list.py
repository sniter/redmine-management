__author__ = 'ilya'

from termcolor import colored
from common import CommonRender


class TaskList(CommonRender):

    def __call__(self, *args, **kwargs):
        connection = kwargs.get('connection', None)
        args = kwargs.get('args', None)

        for issue in connection.issue.filter(project_id=args.project, assigned_to_id='me', limit=args.limit,
                                             sort=args.sort):

            print u' '.join(map(lambda v: u'%s' % v, [
                self._decorate_id(issue.id),
                self._decorate_status(issue.status),
                self._decorate_priority(issue.priority),
                self._decorate_done(issue.done_ratio),
                colored(issue.subject, 'white')
            ]))
            descr = None  # u'%{description}'.format(**dict_issue)

            # for line in twrapper.wrap(subj):
            #     print colored(unicode(line), 'green')
            if descr:
                print colored('-' * self.monitor_width, 'green')
                for line in self.twrapper.wrap(descr):
                    print colored(line, 'white')
