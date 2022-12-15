#!/bin/bash

# ./script.sh -t nombre-del-tag
# ./script.sh -t iteracion5

echo "Ejcutando script"

cd ~
cd Desktop/Backend/PROYECTO_IS2/
DB_NAME="producciondb"
DB_FILE_NAME="desarrollo.sql"

if [ "$1" = "-t" ]; then
	git fetch
	git checkout $2
	echo "Corriendo Programa"
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"
	sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
	echo "Base de datos creada"
	echo "Poblando base de datos"
  	psql -U usuario -W -h localhost -p 5432 $DB_NAME < $DB_FILE_NAME
	echo "Base de datos poblada"
	echo "Corriendo test"
	python3 manage.py test
	echo "Test ejecutados"
	echo "Corriendo servidor de desarrollo"
	python3 manage.py runserver 
fi

# poblar base de datos
if [ "$1" = "-p" ]; then
  echo "Poblar base de datos"
  psql -U usuario -W -h localhost -p 5432 $DB_NAME < $DB_FILE_NAME
fi

# hacer backup de la base de datos
if [ "$1" = "-b" ]; then
   echo "Creando el backup"
   pg_dump -U usuario -W -h localhost -p 5432 $DB_NAME > $DB_FILE_NAME
   echo "Backup creado"
fi
