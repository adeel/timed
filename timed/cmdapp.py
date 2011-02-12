import sys

program = {}
handlers = {}

def main(name, desc, config={}):
  program['name'] = name
  program['desc'] = desc
  
  if len(sys.argv) < 2:
    command, args = '', []
  else:
    command, args = sys.argv[1], sys.argv[2:]
  
  options = config
  for i, arg in enumerate(args):
    if arg.startswith('--'):
      opt = arg.lstrip('--')
      try:
        key, val = opt.split('=')
      except ValueError:
        key = opt.split('=')
        val = True
      options[key] = val
      del args[i]

  if command in handlers:
    handler = handlers[command]
  else:
    handler = help

  try:
    handler(*args, **options)
  except Exception as e:
    print "error: %s" % str(e)

def cmd(handler):
  handlers[handler.__name__] = handler
  return handler

def default(handler):
  handlers[''] = handler
  return handler

def help(**options):
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
