# VR-CLUB
## How to run the project locally?


### 💾 Downloading the project
#### Git clone
```bash
git clone https://github.com/RezenkovD/vr-club.git
```


### 🔨 Dependency installation
Install the dependencies to run the project
#### Libs installation
```bash
pip3 install -r requirements.txt
```


### ⚡️ Setup database
##### Connect to database
```bash
sudo -u postgres psql 
```
##### Setup database
```bash
CREATE DATABASE '<database-name>';
ALTER USER '<database-user>' WITH PASSWORD '<database-password>';
GRANT ALL PRIVILEGES ON DATABASE '<database-name>' TO '<database-user>';
```


### 🔐 Get your SECRET_KEY
Get your secret key. And make changes to the settings
##### Get your secret key
```
https://djecrety.ir/
```


### 🏰 Setting up OAuth 2.0
Get your `<client-id>` and `<client-secret>`
##### Setting up OAuth 2.0
```
https://support.google.com/cloud/answer/6158849
```


### ✉️ Setting Gmail
Get your `<host-password>`
##### How to get app passwords
```
https://support.google.com/mail/answer/185833
```


### 🎁 Setup env
Configure the .env file that contains the variables to run the app and use Google Oauth2 and email to send emails
##### Configure the .env file 
`
Move the contents from example.env to .env and specify your values
`


### 🗃️ Makemigrations
Run the command in the directory with file manage.py
##### Makemigrations writes model changes to separate migration files, similar to commits. Create makemigrations
```bash
python manage.py makemigrations
```


### 🗄️ Migrate
Run the command in the directory with file manage.py
##### Migrate applies these changes to the database. Create migrate
```bash
python manage.py migrate
```


### 👑 Superuser
Run the command in the directory with file manage.py. Follow the instructions
##### Create superuser
```bash
python manage.py createsuperuser
```


### 🚀 Start
Run the command in the directory with file manage.py
##### Run project
```bash
python manage.py runserver
```
