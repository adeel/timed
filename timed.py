import sys
import os.path
import time
import datetime
import yaml
from pkg_resources import Requirement, resource_string

DATA_FILE = os.path.expanduser('~/.timed')
TIME_FORMAT = '[%d %b %Y] %H:%M'
README = resource_string(Requirement.parse('timed'), 'README')

def main():
  if not os.path.exists(DATA_FILE):
    open(DATA_FILE, 'w').close()
    print README
  if len(sys.argv) == 1:
    Controller().default()
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'stop':
      Controller().stop()
    elif sys.argv[1] == 'summary':
      Controller().summary()
    else:
      Controller().start(sys.argv[1])
  elif len(sys.argv) == 3:
    if sys.argv[1] == 'start':
      Controller().start(sys.argv[2])

class Controller(object):
  
  def __init__(self):
    data = open(DATA_FILE).read()
    self.logs = yaml.safe_load(data)
  
  def default(self):
    if self.logs:
      last = self.logs[-1]
      if not last.get('end'):
        print 'working on: %s' % last['project']
        print 'started: %s' % last.get('start')
        print 'time elapsed: %s' % get_elapsed_time(last.get('start'))
      else:
        self.summary()
  
  def summary(self):
    summary = {}
    for log in self.logs:
      if not summary.has_key(log['project']):
        summary[log['project']] = 0
      summary[log['project']] += (Time(log.get('end'))
                                - Time(log.get('start'))).seconds / 60
    
    for project, min in summary.items():
      print "%s: %sh%sm" % (project, min/60, min - 60 * (min/60))
  
  def start(self, project):
    self.logs.append({'project': project, 'start': time.strftime(TIME_FORMAT)})
    self.save()
    print "starting work on %s" % project
  
  def stop(self):
    if not self.logs:
      print "not working on anything"
    else:
      last = self.logs[-1]
      print "stopped working on: %s" % last['project']
      print "--"
      print "started: %s" % last.get('start')
      print "time spent: %s" % get_elapsed_time(last.get('start'))
      
      self.logs[-1]['end'] = time.strftime(TIME_FORMAT)
      self.save()
  
  def save(self):
    open(DATA_FILE, 'w').write(yaml.dump(self.logs, default_flow_style=False))
  

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