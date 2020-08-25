# Powtoons

### Prerequisites

* python3.6
* Django 2.2
* Django Rest Framework 3.8.2
* Postgre SQL 10.12

### Postgre SQL setup
Postgre SQL instalation
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```
Create new DB
```
sudo -u postgres createdb db_name
```
Create postgre sql user
```
sudo -u postgres createuser --interactive
```
### Application setup

Installing needed dependencies
```
pip install-r requirements.txt
```
Making migrations
```
./manage.py migrate
```
Creating superuser for admin
```
./manage.py createsuperuser
```
Loading data from fixtures 
```
python manage.py loaddata fixtures/permission.json --app auth.permission
python manage.py loaddata fixtures/group.json --app auth.group
```
Starting the application:
```
python manage.py runserver
```
