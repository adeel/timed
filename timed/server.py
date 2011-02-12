import datetime
import itertools
from operator import itemgetter

def summarize(records):
  return [(r[0], sum(s[1] for s in r[1])) for r in
    itertools.groupby(sorted(records, key=itemgetter(0)), itemgetter(0))]

def start(project, records):
  return records + [(project, (datetime.datetime.now(), None))]

def stop(records):
  if records and not records[-1][1][1]:
    return records[:-1] + \
      [(lambda r: (r[0], (r[1][0], datetime.datetime.now())))(records[-1])]
  return records

def record_from_txt(line, only_elapsed=False, time_format='%H:%M on %d %b %Y'):
  try:
    def transform(record):
      if only_elapsed:
        return (record[0], minutes_elapsed(
          date_from_txt(record[1][0], time_format),
          date_from_txt(record[1][1], time_format)))
      else:
        return (record[0], (date_from_txt(record[1][0], time_format),
                            date_from_txt(record[1][1], time_format)))

    return transform((lambda project, times: (project.strip(), (
      lambda start, end: (start.strip(), end.strip()))(
        *times.split(' - '))))(*line.split(':', 1)))

  except ValueError:
    raise SyntaxError(line)

def record_to_txt(record, time_format):
  return "%s: %s - %s" % (record[0],
    date_to_txt(record[1][0], time_format),
    date_to_txt(record[1][1], time_format))

def date_from_txt(date, time_format):
  if not date:
    return None
  return datetime.datetime.strptime(date, time_format)

def date_to_txt(date, time_format):
  if not date:
    return ''
  return date.strftime(time_format)

def minutes_elapsed(start, end=None):
  if not end:
    end = datetime.datetime.now()
  return (end - start).seconds / 60

class SyntaxError(Exception):
  def __init__(self, line):
    self.line = line

  def __str__(self):
    return "syntax error on this line:\n  %s" % repr(self.line)
