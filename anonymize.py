#!/usr/bin/python3
# License: GPLv3
# Author: Timothy Hobbs (© auto*mat https://www.auto-mat.cz/)

import json
import sys
import hashlib

if len(sys.argv) != 3:
 sys.exit("""
 This utility is used to psuedo-anonymize json exports userattendances from the do-prace-na-kole django app. The anonymized output is NOT INTENDED FOR EXTERNAL RELEASE! Please analize files before releasing them publicly. Origional intent is for internal analysis only!

Use it by passing a file name and a salt file. The salt file should contain a securely generated random string, perhaps by tailing "/dev/random" or using the mcookie utility.

Ex:

$ ./anonymize.py UserAttendance-2017.json salt_file
""")

salt_file = sys.argv[2]
salt=open(salt_file, 'rb').read()

uas = json.load(open(sys.argv[1]))
for ua in uas:
 personal_info = [
  'company_admin_emails',
  'userprofile__telephone',
  'userprofile__user__email',
  'userprofile__user__first_name',
  'userprofile__user__last_name',
  'userprofile__user__id',
  'userprofile__user__username',
 ]
 for field in personal_info:
  ua[field] = hashlib.sha224(str(ua[field]).encode("utf8")+salt).hexdigest()

json.dump(uas, open(sys.argv[1]+".anon", "w"))
