import sys
import os.path
import time

def list_categories():
  categories = sorted(tuple(set(log.category for log in Log().find())))
  
  for category in categories:
    print category

class Timer:
  
  def __init__(self, name):
    self.name = name
  
  def start(self):
    self.start = time.time()
  
  def stop(self):
    if self.start:
      self.elapsed = time.time() - self.start
      self.start = None
      return self.elapsed
  

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
    if self.id:
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
    if self.id:
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
    list_categories()