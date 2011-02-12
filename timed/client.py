"Timed: a command-line time tracker."

__name__ = 'client'

import sys
import os.path
import datetime
from termcolor import colored

from timed import server
from timed import cmdapp

now = datetime.datetime.now

def main():
  cmdapp.main(name='timed', desc=__doc__, config={
    'logfile': os.path.expanduser('~/.timed'),
    'time_format': '%H:%M on %d %b %Y'})

@cmdapp.cmd
def summary(logfile, time_format):
  "show a summary of all projects"

  def output(summary):
    width = max([len(p[0]) for p in summary]) + 3
    print '\n'.join([
      "%s%s%s" % (p[0], ' ' * (width - len(p[0])),
        colored(minutes_to_txt(p[1]), 'red')) for p in summary])

  output(server.summarize(read(logfile, time_format, only_elapsed=True)))

@cmdapp.cmd
@cmdapp.default
def status(logfile, time_format):
  "show current status"

  try:
    r = read(logfile, time_format)[-1]
    if r[1][1]:
      return summary(logfile, time_format)
    else:
      print "working on %s" % colored(r[0], attrs=['bold'])
      print "  since    %s" % colored(
        server.date_to_txt(r[1][0], time_format), 'green')
      print "  to now,  %s" % colored(
        server.date_to_txt(now(), time_format), 'green')
      print "        => %s elapsed" % colored(time_elapsed(r[1][0]), 'red')
  except IndexError:
    return cmdapp.help()

@cmdapp.cmd
def start(project, logfile, time_format):
  "start tracking for <project>"

  write(server.start(project, read(logfile, time_format)),
    logfile, time_format)

  print "starting work on %s" % colored(project, attrs=['bold'])
  print "  at %s" % colored(server.date_to_txt(now(), time_format), 'green')

@cmdapp.cmd
def stop(logfile, time_format):
  "stop tracking for the active project"

  def save_and_output(records):
    records = server.stop(records)
    write(records, logfile, time_format)

    def output(r):
      print "worked on %s" % colored(r[0], attrs=['bold'])
      print "  from    %s" % colored(
        server.date_to_txt(r[1][0], time_format), 'green')
      print "  to now, %s" % colored(
        server.date_to_txt(r[1][1], time_format), 'green')
      print "       => %s elapsed" % colored(
        time_elapsed(r[1][0], r[1][1]), 'red')

    output(records[-1])

  save_and_output(read(logfile, time_format))

@cmdapp.cmd
def parse(logfile, time_format):
  "parses a stream with text formatted as a Timed logfile and shows a summary"

  records = [server.record_from_txt(line, only_elapsed=True,
    time_format=time_format) for line in sys.stdin.readlines()]

  # TODO: make this code better.
  def output(summary):
    width = max([len(p[0]) for p in summary]) + 3
    print '\n'.join([
      "%s%s%s" % (p[0], ' ' * (width - len(p[0])),
        colored(minutes_to_txt(p[1]), 'red')) for p in summary])

  output(server.summarize(records))

def read(logfile, time_format, only_elapsed=False):
  return [server.record_from_txt(line, only_elapsed=only_elapsed,
    time_format=time_format) for line in open(
      os.path.expanduser(logfile)).readlines()]

def write(records, logfile, time_format):
  try:
    open(logfile, 'w').write('\n'.join(
      [server.record_to_txt(record, time_format) for record in records]))
  except IOError:
    print "error: could not open log file for writing: %s" % logfile

def time_elapsed(start, end=None):
  return minutes_to_txt(server.minutes_elapsed(start, end))

def minutes_to_txt(delta):
  hour = delta / 60
  min = delta - 60 * hour
  return "%sh%sm" % (hour, min)
