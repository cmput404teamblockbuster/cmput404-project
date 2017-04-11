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

## jump through hoops ##
```
change the "site_name" variable at the top of /users/models.py and posts/models.py to be euqal to the desired host name, ex: "http://127.0.0.1:8000/api/" 
```


## After pulling from master ##
There may be migrations that you need to apply. To do by:
```
python manage.py migrate
```

## More hoops ##
```
After migrating for the first time, create a superuser, run the server with and log into the admin panel. Click on "Sites" and change the site name from "example.com" to the desired host name, "http://127.0.0.1:8000/api/". Stop the server and migrate again. optionally change site_name back to what it was before in /users/models.py and posts/models.py. create a new super user named "god".  
```

## Running ##
```
python manage.py runserver
```
open browser to the host name





## our list of live versions
```
blockbuster.canadacentral.cloudapp.azure.com
```

## Contributers:

* https://github.com/AaronHongyangLiu
* https://github.com/cjresler
* https://github.com/Joduro
* https://github.com/tdarnett
* https://github.com/TheAspiredOne
* https://github.com/sam9116

## References Accessed March-April 2017:

* https://medium.com/@rajaraodv/webpack-the-confusing-parts-58712f8fcad9#.4mcf8uagv
* https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
* https://docs.python.org/3.3/library/
* https://www.w3schools.com/
* http://geezhawk.github.io/user-authentication-with-react-and-django-rest-framework
* http://stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework Cahlan Sharp
* http://www.django-rest-framework.org/#api-guide
* http://stackoverflow.com/a/34015469/988941 MoOx
* http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078 Muhammad Usman
* http://factoryboy.readthedocs.io/en/latest/recipes.html?highlight=UserModelFactory

