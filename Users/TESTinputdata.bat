@echo off
cd dataJson
echo act
mongoimport --db test --collection act --file act.json
echo categories
mongoimport --db test --collection categories --file categories.json
echo orgid_counter
mongoimport --db test --collection orgid_counter --file orgid_counter.json
echo users
mongoimport --db test --collection users --file users.json
echo done
pause