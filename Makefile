up:
	docker compose -f docker-compose.yaml up --build -d

down:
	docker-compose -f docker-compose.yaml down

downup:
	make down && make up
