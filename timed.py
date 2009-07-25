import sys
import os.path
import time, datetime
import yaml
import pkg_resources
import cmdapp

DATA_FILE = os.path.expanduser('~/.timed')
TIME_FORMAT = '%H:%M on %d %b %Y'

def main():
  if not os.path.exists(DATA_FILE):
    open(DATA_FILE, 'w').close()  
  cmdapp.main()

@cmdapp.cmd
def help():
  readme = pkg_resources.resource_string(
    pkg_resources.Requirement.parse('timed'), 'README')
  print readme

@cmdapp.cmd
def index():
  logs = read()
  if logs:
    last = logs[-1]
    if not last.get('end'):
      project = last['project']
      start = last.get('start')
      end = datetime.datetime.now()
      print "working on %s:" % project
      print "  from    %s" % start.strftime(TIME_FORMAT)
      print "  to now, %s" % end.strftime(TIME_FORMAT)
      print "       => %s have elapsed" % elapsed_time(start, end)
    else:
      summary()
  else:
    readme()

@cmdapp.cmd
def summary():
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
  logs = read()
  start = datetime.datetime.now()
  logs.append({'project': project, 'start': start})
  save(logs)
  print "starting work on %s" % project
  print "  at %s" % start.strftime(TIME_FORMAT)

@cmdapp.cmd
def stop():
  logs = read()
  if not logs:
    print "error: no active project"
  else:
    last = logs[-1]
    project = last['project']
    start = last.get('start')
    end = datetime.datetime.now()
    print "worked on %s" % project
    print "  from    %s" % start.strftime(TIME_FORMAT)
    print "  to now, %s" % end.strftime(TIME_FORMAT)
    print "       => %s elapsed" % elapsed_time(start)
    
    logs[-1]['end'] = end
    save(logs)

def read():
  data = open(DATA_FILE).read()
  if not data:
    return []
  
  return yaml.safe_load(data)

def save(logs):
  open(DATA_FILE, 'w').write(yaml.dump(logs, default_flow_style=False))

def elapsed_time(start, end=None):
  if not end:
    end = datetime.datetime.now()
  delta = (end - start).seconds
  hour = delta / 3600
  min = (delta - 3600 * hour) / 60
  return '%sh%sm' % (hour, min)

if __name__ == '__main__':
  main()