#!/usr/bin/env bash
python get-pip.py
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
cd code
python manage.py migrate
python manage.py loaddata payroll/fixtures/*.json