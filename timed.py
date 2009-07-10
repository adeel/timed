import time

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
  

