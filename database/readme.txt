--build database
docker build -t gamelend-postgres .

--edit env file to your liking

--create and launch container
docker run --name gamelend-db `
  --env-file .env `
  -p 5432:5432 -d gamelend-postgres



