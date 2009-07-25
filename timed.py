import sys
import os.path
import time, datetime
import yaml
import pkg_resources
import cmdapp

TIME_FORMAT = '[%d %b %Y] %H:%M'
DATA_FILE = os.path.expanduser('~/.timed')

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
      print 'working on: %s' % last['project']
      print 'started: %s' % last.get('start')
      print 'time elapsed: %s' % get_elapsed_time(last.get('start'))
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
    summary[log['project']] += (Time(log.get('end'))
                              - Time(log.get('start'))).seconds / 60
  
  for project, min in summary.items():
    print "%s: %sh%sm" % (project, min/60, min - 60 * (min/60))

@cmdapp.cmd
def start(project):
  logs = read()
  logs.append({'project': project, 'start': time.strftime(TIME_FORMAT)})
  save(logs)
  print "starting work on %s" % project

@cmdapp.cmd
def stop():
  logs = read()
  if not logs:
    print "not working on anything"
  else:
    last = logs[-1]
    print "stopped working on: %s" % last['project']
    print "--"
    print "started: %s" % last.get('start')
    print "time spent: %s" % get_elapsed_time(last.get('start'))
    
    logs[-1]['end'] = time.strftime(TIME_FORMAT)
    save(logs)

def read():
  data = open(DATA_FILE).read()
  if not data:
    return []
  
  return yaml.safe_load(data)

def save(logs):
  open(DATA_FILE, 'w').write(yaml.dump(logs, default_flow_style=False))

def get_elapsed_time(start, end=None):
  delta = (Time(end) - Time(start)).seconds
  hour = delta / 3600
  min = (delta - 3600 * hour) / 60
  return '%s:%s' % (str(hour).rjust(2, '0'), str(min).rjust(2, '0'))

class Time(object):
  
  def __init__(self, strtime=None):
    if strtime:
      self.time = strtime
    else:
      self.time = time.strftime(TIME_FORMAT)
  
  def __sub__(self, time2):
    return self.to_datetime() - time2.to_datetime()
  
  def __str__(self):
    return self.time
  
  def to_datetime(self):
    return datetime.datetime.strptime(self.time, TIME_FORMAT)

if __name__ == '__main__':
  main()