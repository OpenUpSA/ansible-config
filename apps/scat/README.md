# SCAT CRM

See [app repo](https://github.com/OpenUpSA/case-management).

## Environment setup

Create database:

```shell
psql \
   --host=openup-db-rds-postgres13.ca6q5rr6gnmk.af-south-1.rds.amazonaws.com \
   --port=5432 \
   --username=openupadmin \
   --dbname=postgres
# Enter password

# postgres=>
create role scatcrm with login password 'actual-password';
grant scatcrm to openupadmin;
create database scatcrm with owner scatcrm;
```

Deploy environment:

```shell
pass git pull
export PASSWORD_STORE_DIR=~/.pass/openup

# Deploy environment for the first time:
ansible-playbook --inventory inventory/prod.yml apps/scat-crm/backend.yml # --check --diff first

# Deploy app playbook changes:
ansible-playbook --inventory inventory/prod.yml apps/scat-crm/backend.yml --start-at-task "Dokku app exists" --tags app # --check --diff first
```

```shell
ansible hetzner1.openup.org.za -a 'dokku letsencrypt scat-crm-prod'
```
