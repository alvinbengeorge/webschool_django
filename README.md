### Build Server and Database

```bash
$ docker compose build
```

### Start Server and Database

```bash
$ docker compose up -d
```

You can access the server at `localhost:8080`.

### Stop Server and Database

```bash
$ docker-compose stop
```

### Making and Running Migrations

```bash
$ docker compose exec app python manage.py makemigrations
$ docker compose exec app python manage.py migrate
```
