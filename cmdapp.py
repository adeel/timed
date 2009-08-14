import sys

program = {}
handlers = {}

def main(name, desc):
  program['name'] = name
  program['desc'] = desc
  
  if len(sys.argv) < 2:
    command, args = '', []
  else:
    command, args = sys.argv[1], sys.argv[2:]
  
  options = {}
  for i, arg in enumerate(args):
    if arg.startswith('--'):
      opt = arg.lstrip('--')
      options[opt] = True
      del args[i]
  
  if command in handlers:
    handler = handlers[command]
  else:
    handler = help
  
  try:
    handler(*args, **options)
  except Exception as e:
    print e.args

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
