# OLS-VHost-Add

## TODO

- [x] Add new vhost to the OLS configuration
  - [x] Add new vhost to the `vhost` file
  - [x] Add new vhost to the `vhconf` file
- [ ] Add new Lables to the docker-compose file (traefik configuration)
  - `traefik.http.routers.litespeed.rule=Host(``new.vhost.com``)`
- [ ] Restart OpenLiteSpeed docker container
  - `docker compose up -d --force-recreate litespeed`

## Description

Execute the script as a **root** and provide new vhost name and the domains you want to add to the vhost.

## Usage

1. Create virutal environment and activate it
   ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```
2. Install the requirements
   ```shell
    pip install -r requirements.txt
   ```
3. Run the script
   ```shell
    python3 ols-vhost-add.py
   ```
