# DVA200

## Installation
```
pip3 install virtualenv
````
### Mac/Linux
```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip3 install -r deps.txt
```

### Windows
```
virtualenv venv
venv\Scripts\activate
(venv) $ pip3 install -r deps.txt
```

## Körning
```
(venv) $ python3 server.py
* Running on http://127.0.0.1:5000/
* Restarting with reloader
```

## Registrera en användare med curl (sqlalchemy versionen)
```
$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"oscar","password":"dva200"}' http://127.0.0.1:5000/api/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 27
Location: http://127.0.0.1:5000/api/users/1
Server: Werkzeug/1.0.1 Python/3.8.1
Date: Mon, 20 Apr 2020 11:35:39 GMT

{
  "username": "oscar"
}
```

## Begär en auth-token med curl (sqlalchemy versionen)
```
$ curl -u oscar:dva200 -i -X GET http://127.0.0.1:5000/api/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 139
Server: Werkzeug/1.0.1 Python/3.8.1
Date: Mon, 20 Apr 2020 11:37:02 GMT
{
  "duration": 600,
  "token": "byJhbGciOiJIUzI1GiIsImV5cCI6MTM4NTY2OZY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JB1BPzXjSohKYDRT472wGOvjc"
}
```

## Begär en skyddad resurs med curl (sqlalchemy versionen)
```
$ curl -u oscar:dva200 -i -X GET http://127.0.0.1:5000/api/login
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 30
Server: Werkzeug/1.0.1 Python/3.8.1
Date: Mon, 20 Apr 2020 11:36:14 GMT

{
  "data": "Hello, oscar!"
}
```
