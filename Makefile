# Имя контейнера (из docker-compose.yml)
CONTAINER=qwerty9yy/dobslovo-bot

# ====== Docker ======
up:
	docker compose up -d

down:
	docker compose down

rebuild:
	docker compose down
	docker compose up -d --build

logs:
	docker compose logs -f

shell:
	docker exec -it $(CONTAINER) /bin/bash

# ====== Database ======
reset-db:
	rm -f bot/db/db.db
	docker compose up -d --build

# ====== Git ======
pull:
	git pull

push:
	git add .
	git commit -m "update"
	git push
