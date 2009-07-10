import sys
import os.path
import datetime, time

def get_summary():
  summary = {}
  for log in Log().find():
    if not summary.has_key(log.category):
      summary[log.category] = 0
    summary[log.category] += (Time(log.end) - Time(log.start)).seconds / 60
  
  for category, min in summary.items():
    print "%s: %sh%sm" % (category, min/60, min - 60 * (min/60))

def get_elapsed_time(start, end=None):
  delta = (Time(end) - Time(start)).seconds
  hour = delta / 3600
  min = (delta - 3600 * hour) / 60
  return '%s:%s' % (str(hour).rjust(2, '0'), str(min).rjust(2, '0'))

def list_categories():
  categories = sorted(tuple(set(log.category for log in Log().find())))
  
  for category in categories:
    print category
  
  if not categories:
    print "%s <category-name>" % (sys.argv[0])

class Time(object):
  
  def __init__(self, strtime=None):
    if strtime:
      self.time = strtime
    else:
      self.time = time.strftime('%H:%M')
  
  def __sub__(self, time2):
    return self.to_datetime() - time2.to_datetime()
  
  def __str__(self):
    return self.time
  
  def to_datetime(self):
    hour, minute = (int(x) for x in self.time.split(':'))
    return datetime.datetime.now().replace(hour=hour, minute=minute,
                                           second=0, microsecond=0)
  

class Log(object):
  
  source = os.path.expanduser('~/.timed')
  
  def __init__(self, **fields):
    self.id = fields.get('id')
    self.category = fields.get('category')
    self.start = fields.get('start')
    self.end = fields.get('end')
  
  def find(self, category=None):
    results = []
    
    lines = open(self.source).readlines()
    for id, line in enumerate(lines):
      fields = line.split()

      if not len(fields) == 3:
        break

      if category and category != fields[0]:
        continue

      if fields[2] == '-':
        fields[2] = None

      results.append(Log(id=id, category=fields[0], start=fields[1],
                                                      end=fields[2]))
    
    return results
  
  def save(self):
    if self.id is not None:
      return self.update()
    
    if all((self.category, self.start)):
      self.id = len(open(self.source).readlines())
      
      if self.end:
        end = self.end
      else:
        end = '-'
      line = '%s %s %s\n' % (self.category, self.start, end)
      
      open(self.source, 'a').write(line)
      
      return self.id
  
  def update(self):
    if self.id is not None:
      lines = open(self.source).readlines()
      line = lines[self.id].split()
      
      if self.end:
        end = self.end
      else:
        end = '-'
      lines[self.id] = '%s %s %s\n' % (self.category, self.start, end)

      open(self.source, 'w').write(''.join(lines))
  
  def __repr__(self):
    return str({'id': self.id, 'category': self.category, 'start': self.start,
                'end': self.end})
  
if __name__ == '__main__':
  
  if len(sys.argv) == 1:
    logs = Log().find()
    if logs:
      last = logs[-1]
      if not last.end:
        print 'working on: %s' % last.category
        print 'started: %s' % last.start
        print 'time elapsed: %s' % get_elapsed_time(last.start)
      else:
        get_summary()
    
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'stop':
      logs = Log().find()
      if not logs:
        print "not working on anything"
      else:
        last = logs[-1]
        print last.id
        print 'stopped working on: %s' % last.category
        print '--'
        print 'started: %s' % last.start
        print 'time spent: %s' % get_elapsed_time(last.start)

        last.end = time.strftime('%H:%M')
        last.save()
    elif sys.argv[1] == 'summary':
      get_summary()
    else:
      Log(category=sys.argv[1], start=time.strftime('%H:%M')).save()
