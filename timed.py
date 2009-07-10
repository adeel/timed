import sys
import os.path
import datetime, time

def get_elapsed_time(since):
  hour, min = (int(x) for x in since.split(':'))
  now = datetime.datetime.now()
  then = datetime.datetime(now.year, now.month, now.day, hour, min)
  
  delta = (now - then)
  hour = delta.seconds / 3600
  min = (delta.seconds - 3600 * hour) / 60
  return '%s:%s' % (hour, min)

def list_categories():
  categories = sorted(tuple(set(log.category for log in Log().find())))
  
  for category in categories:
    print category
  
  if not categories:
    print "%s <category-name>" % (sys.argv[0])

class Log:
  
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
    return str({'id': self.id, 'category': self.category, 'start': self.start, 'end': self.end})
  
if __name__ == '__main__':
  
  if len(sys.argv) == 1:
    logs = Log().find()
    if logs:
      last = logs[-1]
      if not last.end:
        print 'working on: %s' % last.category
        print 'started: %s' % last.start
        print 'time elapsed: %s' % get_elapsed_time(last.start)
        exit()
    print 'not working on anything'
    if Log().find():
      print
      print '--'
      print '\n'.join("%s %s %s" % (log.category, log.start, log.end) for log in Log().find()[-5:])
    
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'stop':
      logs = Log().find()
      if not logs:
        print "You need to start first."
      else:
        last = logs[-1]
        print last.id
        print 'stopped working on: %s' % last.category
        print '--'
        print 'started: %s' % last.start
        print 'time spent: %s' % get_elapsed_time(last.start)

        last.end = time.strftime('%H:%M')
        last.save()
    else:
      Log(category=sys.argv[1], start=time.strftime('%H:%M')).save()
