#!/bin/bash

# ./script.sh -t nombre-del-tag
# ./script.sh -t iteracion5

echo "Ejcutando script"

cd ~
cd ~/Desktop/Backend/PROYECTO_IS2/
DB_NAME="agileproject"
DB_FILE_NAME="produccion.sql"

if [ "$1" = "-t" ]; then

	git fetch
	git checkout $2

	echo "Corriendo Programa"
	#pg_dump -U usuario -W -h localhost -p 5432  $DB_NAME > $DB_FILE_NAME
	#python3 manage.py migrate
	psql -U usuario -W -h localhost -p 5432 $DB_NAME < $DB_FILE_NAME

	echo "Base de datos creada"
	python3 manage.py test
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