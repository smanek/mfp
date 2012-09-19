#!/usr/bin/env python

import argparse
import xml.etree.ElementTree as ET

DEFAULT_INPUT = '365.xml'
DEFAULT_CSV_OUTPUT = '365.csv'

def parse(f):
  tree = ET.parse(f)
  root = tree.getroot()
  chartData = root.find('chart_data')
  (dates, weights) = chartData.findall('row')

  assert len(dates) == len(weights)
  raw = [(date.text, weight.text) for (date, weight) in zip(dates, weights)]
  filtered = []

  # add day numbers to the entries (easier to do here, than post filtering)
  for i in xrange(len(raw)):
    raw[i] = (i, raw[i][0], raw[i][1])
  
  # filter dupes and empties
  prevWeight = '0.0'
  for (num, date, weight) in raw:
    if weight != '0.0' and weight != prevWeight and weight is not None:
      filtered.append((num, date, weight))
      prevWeight = weight
  
  # normalize the day numbers, so the first entry is day 1
  offset = filtered[0][0] - 1
  return [(n - offset, date, weight) for (n, date, weight) in filtered]


def dumpcsv(weights, outputfile):
  with open(outputfile, 'w') as out:
    for (day, date, weight) in weights:
      out.write("%s, %s, %s\n" % (day, date, weight))


def main():
  parser = argparse.ArgumentParser(description='Analyze the xml dump from MyFitnessPal (http://www.myfitnesspal.com/reports/results/progress/1/365)')
  parser.add_argument('--input', dest='input', help="the XML input file (default %s)" % DEFAULT_INPUT, default=DEFAULT_INPUT)
  parser.add_argument('-outcsv', dest='outputcsv', help="the CSV output file (default %s)" % DEFAULT_CSV_OUTPUT, default=DEFAULT_CSV_OUTPUT)
  args = parser.parse_args()

  weights = parse(args.input)
  dumpcsv(weights, args.outputcsv)


if __name__ == '__main__':
  main()
