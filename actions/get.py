__author__ = 'ilya'


from termcolor import colored
from common import CommonRender, _res_to_dict


class TaskGet(CommonRender):

    def __call__(self, *args, **kwargs):
        connection = kwargs.get('connection', None)
        args = kwargs.get('args', None)

        issue = connection.issue.get(args.id)

        # dict_issue = _res_to_dict(issue)

        print u' '.join(map(lambda v: u'%s' % v, [
            self._decorate_id(issue.id),
            self._decorate_status(issue.status),
            self._decorate_priority(issue.priority),
            self._decorate_done(issue.done_ratio),
            colored(issue.subject, 'white')
        ]))

        # descr = u'%{description}'.format(**dict_issue)
        print colored('-' * self.monitor_width, 'green')
        for line in self.twrapper.wrap(issue.description):
            print colored(line, 'white')
