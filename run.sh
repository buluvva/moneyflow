sudo docker network create --subnet 192.168.10.0/24 bot-net-dev

sudo docker run --rm \
--name postgres-dev \
-e POSTGRES_PASSWORD=admin \
-e POSTGRES_USER=admin \
-e POSTGRES_DB=data \
-d \
--network bot-net-dev \
--ip 192.168.10.100 \
-p 5432:5432 \
-v $HOME/data/postgres:/var/lib/postgresql/data postgres

sudo docker run  -d --name bot-dev --rm --network bot-net-dev --ip 192.168.10.200 bot:dev
