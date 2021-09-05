# Alarstudios

## Cloning & Run

1. Clone the project on your PC

```
```   

2. Setup `.env` with your own environment

```
```   

### Local development Docker

1. Build and run docker image

```
docker-compose up --build
```

2. Migrate database

```
docker-compose exec web sh 
alembic upgrade head
```

## Urls

List users

```
GET http://0.0.0.0:8000/
```

Add user

```
POST http://0.0.0.0:8000/users/
```

Edit user

```
POST http://0.0.0.0:8000/users/:user_id
```

List test data

```
GET http://0.0.0.0:8000/datas/
```

### Documentation

Swagger

```
http://0.0.0.0:8000/docs
```

Redoc

```
http://0.0.0.0:8000/redoc
```


