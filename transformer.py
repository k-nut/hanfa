import sys
import json

while True:
  line = sys.stdin.readline()
  if not line:
    break
  raw_record = json.loads(line)

  licence_record = {
    "company_name": raw_record['Name'],
    "company_jurisdiction": 'Croatia',
    "source_url": raw_record['source_url'],
    "sample_date": raw_record['sample_date'],
    "jurisdiction_classification": 'Investment Firm',
    "category": 'Financial',
    "confidence": 'HIGH',
  }

  print json.dumps(licence_record)
