__author__ = 'ilya'

import argparse
from redmine import Redmine
from actions import TaskList, TaskGet

import yaml
import pprint

from os import path
from kitchen.text.converters import getwriter
import sys

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

pp = pprint.PrettyPrinter(indent=2)

stream = file(path.expanduser('~/.redmine'), 'r')
cfg = yaml.load(stream)


def tasks(conn, params):
    task = TaskList()
    task(connection=conn, args=params)

def get_task(conn, params):
    task = TaskGet()
    task(connection=conn, args=params)


parser = argparse.ArgumentParser(description='Redmine Manager.')

parser.add_argument("--host",
                    action="store", dest="host", default=cfg['host'],
                    help="Redmine Login")


parser.add_argument("--login",
                    action="store", dest="login", default=cfg['login'],
                    help="Redmine Login")

parser.add_argument("--password",
                    action="store", dest="password", default=cfg['password'],
                    help="Redmine Password")

parser.add_argument('-p', '--project',
                    action="store", dest="project", default=cfg.get('project', None),
                    help="Redmine Project")

subparsers = parser.add_subparsers(help='sub-command help')


# ----------------------------------------------------------------------------------------------------------------------
list_parser = subparsers.add_parser('list', help='list help')
list_parser.set_defaults(func=tasks)

list_parser.add_argument("--offset",
                         dest='offset', type=int, default=10,
                         help="Offset")

list_parser.add_argument("--limit",
                         dest='limit', type=int, default=10,
                         help="Limit")

list_parser.add_argument("--sort",
                         dest='sort', default='done_ratio:asc, priority:desc',
                         help="Sorting")


# ----------------------------------------------------------------------------------------------------------------------
get_parser = subparsers.add_parser('get', help='get tes info help')
get_parser.set_defaults(func=get_task)

get_parser.add_argument("--id",
                        dest='id', type=int,
                        help="Task Number")



args = parser.parse_args()
redmine = Redmine(unicode(args.host),  username=unicode(args.login), password=unicode(args.password))
args.func(redmine, args)

# pp.pprint(args)
