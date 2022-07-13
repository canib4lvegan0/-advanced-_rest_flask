## Repository dedicated to study of Advanced REST APIs with Flask and Python

My goal with this course was to be able to work with Flask RESTFul...


---


### Running locally

To execute this application locally, go ahead with:

`python3 App.py`

For test them, check http://127.0.0.1:5000 on web browser or Postman. 


### Deploying and Running on Heroku

For correct running on Heroku, the `uwsgi.ini` must be configured.

#### Deploying

First check if target branch (main) is already sets, case not, set them. Then, update the main branch. 
Finally, case "Automatic deploy" is enabled, just check Latest activity to see if deploy was run, or then run the manual deploy.

#### Running

For test them, check https://flaskcourse3.herokuapp.com on web browser or Postman.

#### Heroku CLI
To see realtime logs from Heroku application
- `heroku logs --app flaskcourse3 --tail`


### Deploying and Running on Digital Ocean

For correct running on Heroku, the `uwsgi.ini`, that this project as named `uwsgi.digitalOcean.ini` must be configured
and, after deploy, renamed to `uwsgi.ini`, case this file has been changed.

#### Deploying
The first thing to do is update the repository with the target version that will be deployed to Digital Ocean.
Now, stop the uwsgi and nginx by:
- `sudo systemctl stop uwsgi_items_rest`
- `sudo systemctl stop nginx`

Next step is open Digital Ocean console, enter the source folder and delete the old code `$ cd /var/www/html/items-rest/`. 
After that, clone the repository into root server, and adjust name from`uwsgi.DigitalOcean.ini` to `uwsgi.ini`.

Finally, restart the servers with:
- `sudo systemctl reload nginx`
- `sudo systemctl restart nginx`
- `sudo systemctl status nginx` to check status of the nginx 
Similarly  to uwsgi
- `sudo systemctl start uwsgi`
- `sudo systemctl status uwsgi` to check status of the uwsgi

#### Config files
To configure Nginx and uWSGI services, the respectively config files can be accessed via
- `sudo vi /etc/systemd/system/uwsgi_items_rest.service`
- `sudo vi /etc/systemd/system/uwsgi_items_rest.service`
Nonetheless, the server setting can be accessed via 
- `sudo vi /etc/nginx/sites-enabled/items-rest.conf`

#### Running
Now, after all configured, go ahead to check on browser or postman https://www.canib4lvegan0.com/

#### Viewing the logs
Nginx logs:
- ```sudo vi /var/www/html/items-rest/log/uwsgi.log```
- ```sudo vi /var/www/html/items-rest/log/emperor.log```

uWSGI logs:
- ```sudo vi /var/log/nginx/access.log```
- ```sudo vi /var/log/nginx/error.log```

#### Digital Ocean CLI
To log in on Digital Ocean via local terminal
- `ssh USER@SERVER_IP`

### Environment variables
- `ENVIRONMENT`
- `ADMIN` used to determine how are user admin (by id)
- `FLASK_ENV`
- `CREATE_TABLES` to tell if the tables needs to be created in the first request

### Testing on Postman
Inside the `/docs` folder there is the Postman of the project.
The jwt tokens are captured after login or refresh, and so stored on jwt_tokens variables. 

### Miscellaneous
A command to kill an annoying process from Postman that lock app running via Pycharm
- ```ps -ef | grep ControlCe | grep -v grep | awk '{print $2}' | xargs kill```