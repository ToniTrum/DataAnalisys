docker compose down -v --remove-orphans
docker compose up -d redash_postgres
docker compose run --rm redash_server create_db
docker compose up -d