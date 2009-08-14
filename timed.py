"timed: a command-line time tracker"

__name__ = 'timed'
__author__ = 'Adeel Ahmad Khan'

import sys
import os.path
import time, datetime
import cmdapp

log_file = os.path.expanduser('~/.timed')
time_format = '%H:%M on %d %b %Y'

def main():
  if not os.path.exists(log_file):
    open(log_file, 'w').close()  
  
  cmdapp.main(name=__name__, desc=__doc__)

def help():
  cmdapp.help()

@cmdapp.cmd
@cmdapp.default
def status(quiet=False):
  "print current status"
  
  logs = read()
  if logs:
    last = logs[-1]
    if not last.get('end'):
      project = last['project']
      start = last.get('start')
      end = datetime.datetime.now()
      
      if not quiet:
        print "working on %s:" % project
        print "  from    %s" % start.strftime(time_format)
        print "  to now, %s" % end.strftime(time_format)
        print "       => %s have elapsed" % elapsed_time(start, end)
      else:
        print project
    else:
      if not quiet:
        summary()
  else:
    if not quiet:
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

def elapsed_time(start, end=None):
  if not end:
    end = datetime.datetime.now()
  delta = (end - start).seconds
  hour = delta / 3600
  min = (delta - 3600 * hour) / 60
  return '%sh%sm' % (hour, min)

def read():
  logs = []
  with open(log_file) as data:
    try:
      for line in data:
        project, line = line.split(':', 1)
        project = project.strip()
        
        start, end = line.split(' - ')
        start, end = start.strip(), end.strip()
        
        if not project or not start:
          raise SyntaxError()
        
        start = datetime.datetime.strptime(start, time_format)
        if end:
          end = datetime.datetime.strptime(end, time_format)
        
        if end:
          logs.append({'project': project, 'start': start, 'end': end})
        else:
          logs.append({'project': project, 'start': start})
        
    except ValueError:
      raise SyntaxError()
  
  return logs

def save(logs):
  file = open(log_file, 'w')
  
  def format(log):
    if log.get('end'):
      return '%s: %s - %s' % (log['project'],
        log['start'].strftime(time_format),
        log['end'].strftime(time_format))
    else:
      return '%s: %s - ' % (log['project'],
        log['start'].strftime(time_format))
  
  dump = '\n'.join((format(log) for log in logs))

  file.write(dump)
  file.close()

class SyntaxError(Exception):
  args = 'Syntax error in ~/.timed'

if __name__ == '__main__':
  main()
