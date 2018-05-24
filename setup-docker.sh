docker-compose -f docker-compose.yml run --rm server create_db
docker-compose -f docker-compose.yml run --rm postgres psql -h postgres -U postgres -c "create database tests"
wget localhost:5000/setup --post-data="name=Ashley McTest&email=ashley@example.com&password=REPLACE ME&org_name=default" -O /dev/null
