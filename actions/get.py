__author__ = 'ilya'


from termcolor import colored
from common import CommonRender, _res_to_dict
import pprint

_pp = pprint.PrettyPrinter(indent=2)


class TaskGet(CommonRender):

    def __init__(self):
        super(TaskGet,self).__init__()
        self.priority_tpl = u'%s'
        self.done_tpl = u'%s'
        self.status_tpl = u'%s'


    def _decorate_time_entry(self,time_entry):
        print u' [ {spent_on} ] @ {activity} {hours}: {comments}'.format(**{
            'spent_on': colored(time_entry.get('spent_on', None), 'white'),
            'activity': colored(time_entry.get('activity', {}).get('name',None).ljust(12), 'blue'),
            'hours': colored('%s hours' % time_entry.get('hours', None), 'green'),
            'comments': time_entry['comments'] if len(time_entry.get('comments', 'N/A')) else 'N/A',
        })

    def _decorate_journal(self, journal_record):
        value = journal_record.get('notes',None)
        if value is not None:
            print u'- %s' % value

    def _decorate_issue(self, connection, issue):
        print u'%s  %s ' % (self._decorate_id(issue.id), self._decorate_subject(issue.subject))
        print colored('-' * self.monitor_width, 'green')
        tpl = u'%15s: %s '
        if hasattr(issue, 'status'):
            print tpl % ('Status', self._decorate_status(issue.status))
        if hasattr(issue, 'priority'):
            print tpl % ('Priority', self._decorate_priority(issue.priority))
        if hasattr(issue, 'done_ratio'):
            print tpl % ('Done', self._decorate_done(issue.done_ratio))
        if hasattr(issue, 'spent_hours'):
            print tpl % ('Time Spent', issue.spent_hours)
        if hasattr(issue, 'start_date'):
            print tpl % ('Started', issue.start_date)
        if hasattr(issue, 'created_on'):
            print tpl % ('Created', issue.created_on)
        if hasattr(issue, 'updated_on'):
            print tpl % ('Updated', issue.updated_on)
        if hasattr(issue, 'author'):
         print tpl % ('Author', issue.author)
        if hasattr(issue, 'assigned_to'):
          print tpl % ('Assignee', issue.assigned_to)
        if hasattr(issue, 'fixed_version'):
           print tpl % ('Version', issue.fixed_version)

        # descr = u'%{description}'.format(**dict_issue)

        if hasattr(issue, 'spent_hours'):
            print colored('-' * self.monitor_width, 'green')
            print colored('Time Log:', 'green', attrs=['bold'])
            map(lambda v: self._decorate_time_entry(v), issue.time_entries.values('spent_on', 'hours', 'activity', 'comments'))

        # if hasattr(issue, 'journals'):
        #     print colored('-' * self.monitor_width, 'green')
        #     print colored('Comments:', 'green', attrs=['bold'])
        #     map(lambda v: self._decorate_journal(connection.note.get(v['id'])), issue.journals.values('id'))

        print colored('-' * self.monitor_width, 'green')
        for line in self.twrapper.wrap(issue.description):
            print colored(line, 'white')

    def __call__(self, *args, **kwargs):
        connection = kwargs.get('connection', None)
        args = kwargs.get('args', None)

        issue = connection.issue.get(args.id)

        if hasattr(args, 'progress') and args.progress:
            issue.done_ratio = args.progress
            issue.save()
        if hasattr(args, 'task_status'):
            # redmine_status = connection.statuses.get(args.task_status)
            issue.status = args.task_status
            issue.save()

        dict_issue = _res_to_dict(issue)
        # _pp.pprint(dict_issue)

        self._decorate_issue(connection, issue)
