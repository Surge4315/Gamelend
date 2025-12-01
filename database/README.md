# Gamelend Postgres Database

Instructions on how to build the database

1. **Building the image**
   ```powershell
   docker build -t fleetify-postgres database
   ```

3. **Configure credentials**
   Edit the .env file

4. **Create and run the container**
   
   ```powershell
   docker run --name gamelend-db `
     --env-file .env `
     -p 5432:5432 -d gamelend-postgres
   ```
