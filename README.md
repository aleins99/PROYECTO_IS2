# Agile Project
Este es un gestor de proyectos Agile que te permitirá gestionar proyectos y tareas utilizando metodologías como Scrum o Kanban. 

## Requisitos
Antes de comenzar, asegúrese de tener instalado lo siguiente en su máquina:

* Python 3.x
* PostgreSQL
* Pip (el gestor de paquetes de Python)
* Una cuenta de Google para utilizar su servicio de autenticación

## Instalación
1. Clonar el repositorio:
``` bash
 git clone https://github.com/aleins99/PROYECTO_IS2.git
 cd PROYECTO_IS2
``` 
2. Crear un entorno virtual e instalar las dependencias:
``` bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
3. Configurar la base de datos PostgreSQL:
* Crear una base de datos en PostgreSQL para el proyecto.
* En el archivo settings.py de Django, modificar la sección DATABASES para que tenga los siguientes valores:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nombre_de_la_base_de_datos',
        'USER': 'usuario_de_postgresql',
        'PASSWORD': 'contraseña_de_postgresql',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Configurar la autenticación de Google:
* Crear una cuenta de Google Cloud y crear un proyecto.
* Habilitar la API de autenticación de Google.
* Crear un ID de cliente OAuth 2.0 

5. Aplicar las migraciones de Django:
``` bash
python manage.py migrate
```
6. Ejecutar el servidor de desarrollo:
``` bash
python manage.py runserver
```


### Uso
Una vez que el servidor de desarrollo esté en ejecución, puede acceder a la aplicación en http://localhost:8000. Para iniciar sesión utilizando la autenticación de Google, haga clic en el botón "Iniciar sesión con Google" en la página de inicio.

