# cmput404-project

API docs available at ```/api/docs```

## Create environment ##
Run these commands in the root folder
```
virtualenv venv
source venv/bin/activate
```

## Install dependencies ##
```
pip install -r requirements.txt
npm install
./node_modules/.bin/webpack --config webpack.config.js
```


## After pulling from master
There may be migrations that you need to apply. To do by:
```
python manage.py migrate
```

## Running
```
python manage.py runserver
```
open browser to http://127.0.0.1:8000/





## our list of live versions
```
http://warm-hollows-14698.herokuapp.com
http://radiant-beyond-17792.herokuapp.com
```
