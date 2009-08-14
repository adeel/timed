#!/usr/bin/env python

"Converts a timed-0.11-style log file to a timed-0.12-style log file."

import timed
import yaml

def read():
  data = open(timed.log_file).read()
  if not data:
    return []
  
  return yaml.safe_load(data)
 
logs = read()

timed.save(logs)