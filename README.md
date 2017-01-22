# flask-datatable
a simple flask website, a class wrapped for jquery datatable server-side processing, using sqlalchemy orm

# how to run
1. create virtualenv and activate
2. install package and flask plugin  
   (venv)$pip install -r requirements.txt  
3. create db and testing data  
   (venv)$python manage.py db init  
   (venv)$python manage.py db migrate  
   (venv)$python manage.py db upgrade  
   (venv)$python manage.py shell  
    >>> Student.generate_fake(1000)
4. run the website  
   (venv)$python manage.py runserver
