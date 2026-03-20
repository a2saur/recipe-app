#!/bin/bash

rm -rf migrations
rm meal_planner.db
echo "Removed migrations folder and db"

flask db init
flask db migrate -m "recreated db via shell script"
flask db upgrade
echo "Recreated empty db"

# cd setup-files
# python3 make_initialize_db_info_script.py
# python3 initialize_db_info.py
# cd ..
echo "Done"