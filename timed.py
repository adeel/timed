"timed: a command-line time tracker"

__name__ = 'timed'
__author__ = 'Adeel Ahmad Khan'

import sys
import os.path
import time, datetime
import yaml
import cmdapp

data_file = os.path.expanduser('~/.timed')
time_format = '%H:%M on %d %b %Y'

def main():
  if not os.path.exists(data_file):
    open(data_file, 'w').close()  
  
  cmdapp.main(name=__name__, desc=__doc__)

def help():
  cmdapp.help()

@cmdapp.cmd
@cmdapp.default
def status():
  "print current status"
  
  logs = read()
  if logs:
    last = logs[-1]
    if not last.get('end'):
      project = last['project']
      start = last.get('start')
      end = datetime.datetime.now()
      print "working on %s:" % project
      print "  from    %s" % start.strftime(time_format)
      print "  to now, %s" % end.strftime(time_format)
      print "       => %s have elapsed" % elapsed_time(start, end)
    else:
      summary()
  else:
    help()

@cmdapp.cmd
def summary():
  "print a summary of hours for all projects"
  
  logs = read()
  summary = {}
  for log in logs:
    if not summary.has_key(log['project']):
      summary[log['project']] = 0
    end = log.get('end', datetime.datetime.now())
    start = log.get('start')
    summary[log['project']] += (end - start).seconds / 60
  
  for project, min in summary.items():
    print "  - %s: %sh%sm" % (project, min/60, min - 60 * (min/60))

@cmdapp.cmd
def start(project):
  "start tracking for <project>"
  
  logs = read()
  start = datetime.datetime.now()
  logs.append({'project': project, 'start': start})
  save(logs)
  print "starting work on %s" % project
  print "  at %s" % start.strftime(time_format)

@cmdapp.cmd
def stop():
  "stop tracking for the current project"
  
  logs = read()
  if not logs:
    print "error: no active project"
  else:
    last = logs[-1]
    project = last['project']
    start = last.get('start')
    end = datetime.datetime.now()
    print "worked on %s" % project
    print "  from    %s" % start.strftime(time_format)
    print "  to now, %s" % end.strftime(time_format)
    print "       => %s elapsed" % elapsed_time(start)
    
    logs[-1]['end'] = end
    save(logs)

def read():
  data = open(data_file).read()
  if not data:
    return []
  
  return yaml.safe_load(data)

def save(logs):
  open(data_file, 'w').write(yaml.dump(logs, default_flow_style=False))

def elapsed_time(start, end=None):
  if not end:
    end = datetime.datetime.now()
  delta = (end - start).seconds
  hour = delta / 3600
  min = (delta - 3600 * hour) / 60
  return '%sh%sm' % (hour, min)

if __name__ == '__main__':
  main()
