#!/bin/bash

# ./script.sh -t nombre-del-tag
# ./script.sh -t iteracion5

echo "Ejcutando script"

cd ~
cd Desktop/IS2/PROYECTO_IS2/

if [ "$1" = "-t" ]; then

	git fetch
	#git checkout $2

	DB_NAME="producciondb"
	DB_FILE_NAME="desarrollo.sql"

	#psql -h localhost -p 5432  -U usuario $DB_NAME < $DB_FILE_NAME	 # poblar BD

	python3 manage.py runserver
fi
