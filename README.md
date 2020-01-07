# Paranuara

## Installation 

### Install dependencies

```
pip install -r requirements.txt
```

### Set up MySQL

The sample files (`paranuara/settings_local.py.sample` and `my.cnf.sample`) 
can be used for a MySQL database named paranuara running on localhost, port 3306.


```
cp paranuara/settings_local.py.sample paranuara/settings_local.py
vi my.cnf
```

Once the database is set, run the migrations

```
python manage.py migrate
```

### Load People and companies

Run the following command to load existing data

``` 
python manage.py load_data --companies resources/companies.json --people resources/people.json 
```

### Setup server

gunicorn is on the list of required dependencies. Run the server using:

```
gunicorn myproject.wsgi
```
