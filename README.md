## Wagtail - Vue:
The initial environment of full-stack local dev web app with wagtail and vue.
A demo to show how to use .vue files inside django app.
(bref: change setting of vue.config.js for exporting output files to the directory where django collect the static file)
## Build with:
```
- django: v.3
- wagtail: v.2.14
- wagtail internationalisation
- postgres: 11
- Vue3
- redis:3.0
- elasticsearch:5.4
- docker
```
## Run app:
```
docker-compose build
```
```
docker-compose up
```
App run on:
```
http://localhost:8000/
http://localhost:8000/admin
user: admin
password: changeme
```
