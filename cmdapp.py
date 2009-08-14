import sys

program = {}
handlers = {}

def main(name, desc):
  program['name'] = name
  program['desc'] = desc
  
  if len(sys.argv) < 2:
    command, arguments = '', []
  else:
    command, arguments = sys.argv[1], sys.argv[2:]
  
  if command in handlers:
    handler = handlers[command]
  else:
    handler = help
  
  try:
    handler(*arguments)
  except Exception as e:
    print e.value

def cmd(handler):
  handlers[handler.__name__] = handler
  return handler

def default(handler):
  handlers[''] = handler
  return handler

def help():
  subcmds = []
  for name, handler in handlers.items():
    syntax = (program['name'] + ' ' + name).strip()
    usage = '  %s: %s' % (syntax, handler.__doc__)
    subcmds.append(usage)
  subcmds = '\n'.join(subcmds)
  
  doc = """%s

Usage:
%s""" % (program['desc'], subcmds)
  
  print doc
