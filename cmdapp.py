import sys

handlers = {}

def main():
  if len(sys.argv) < 2:
    command = 'index'
    arguments = []
  else:
    command, arguments = sys.argv[1], sys.argv[2:]
  if command in handlers:
    handler = handlers[command]
  else:
    handler = handlers['index']
  try:
    handler(*arguments)
  except:
    handlers['help']()

def cmd(handler):
  handlers[handler.__name__] = handler
  return handler
