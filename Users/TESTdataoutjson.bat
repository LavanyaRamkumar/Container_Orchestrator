@echo off
cd dataJson
echo deleting old data
rm -rf *
echo deleted
echo act
mongoexport --db cc_assignment --collection act --out act.json
echo categories
mongoexport --db cc_assignment --collection categories --out categories.json
echo orgid_counter
mongoexport --db cc_assignment --collection orgid_counter --out orgid_counter.json
echo users
mongoexport --db cc_assignment --collection users --out users.json
echo done
pause