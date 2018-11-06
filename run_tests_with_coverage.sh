#!/usr/bin/env bash
dir="`dirname $0`"
#echo "The script you are running has basename `basename $0`, dirname `dirname $0`"
#echo "The present working directory is `pwd`"
coverage run --rcfile=${dir}/coverage.conf  manage.py test payroll --settings=settings.test
coverage html --rcfile=${dir}/coverage.conf

