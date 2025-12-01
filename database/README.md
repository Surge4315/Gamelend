# Gamelend Postgres Database

Instructions on how to build the database

1. **Building the image**
   ```powershell
  docker build -t gamelend-postgres .
  ```

2. **Configure credentials**
   Edit the .env file

3. **Create and run the container**
   
   ```powershell
   docker run --name gamelend-db `
     --env-file .env `
     -p 5432:5432 -d gamelend-postgres
   ```
