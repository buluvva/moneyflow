sudo docker run --rm \
--name postgres \
-e POSTGRES_PASSWORD=admin \
-e POSTGRES_USER=admin \
-e POSTGRES_DB=data \
-d \
-p 5432:5432 \
-v $HOME/data/postgres:/var/lib/postgresql/data postgres