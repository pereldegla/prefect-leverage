
# Dev Toolkit

To help developer to have all stack in local, we provide a docker-compose.yaml file with :

- Minio
- Postgres
- 2 Rest Catalog (Raw and Table)
- and a start kit to create databases and buckets

To use it, go to dev-toolkit folder and run :

````shell script
docker compose up -d --build
````

You need to install Docker Desktop before !