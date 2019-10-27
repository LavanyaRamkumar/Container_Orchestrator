cd dataJson
echo act
mongoimport --db cc_assignment --collection act --file act.json
echo categories
mongoimport --db cc_assignment --collection categories --file categories.json
echo orgid_counter
mongoimport --db cc_assignment --collection orgid_counter --file orgid_counter.json
echo users
mongoimport --db cc_assignment --collection users --file users.json
echo done
