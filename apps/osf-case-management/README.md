# OSF Case Management

See [app repo](https://github.com/OpenUpSA/case-management).

## Environment setup

Create database:

```shell
psql \
   --host=postgresql11-prod.cnc362bhpvfe.eu-west-1.rds.amazonaws.com \
   --port=5432 \
   --username=openupadmin \
   --dbname=postgres
# Enter password

# postgres=>
create role osfcasemanagement with login password 'actual-password';
grant osfcasemanagement to openupadmin;
create database osfcasemanagement with owner osfcasemanagement;
```

Add secrets to `secrets_store`:

```shell
pass git pull
pass generate --no-symbols apps/osf-case-management/prod/DJANGO_SECRET_KEY 40
pass insert --multiline apps/osf-case-management/prod/POSTGRES

# Enter:

actual-password
hostname: postgresql11-prod.cnc362bhpvfe.eu-west-1.rds.amazonaws.com
username: osfcasemanagement
database: osfcasemanagement

pass git push
```

Deploy environment:

```shell
pass git pull
export PASSWORD_STORE_DIR=~/.pass/openup

# Deploy environment for the first time:
ansible-playbook --inventory inventory/prod.yml apps/osf-case-management/backend.yml # --check --diff first

# Deploy app playbook changes:
ansible-playbook --inventory inventory/prod.yml apps/osf-case-management/backend.yml --start-at-task "Dokku app exists" --tags app # --check --diff first
```

Set up domain:

On [Cloudflare](https://www.cloudflare.com), add a DNS-only CNAME record 'casemanagement' for openup.org.za pointing to hetzner1.openup.org.za, then run:

```shell
ansible hetzner1.openup.org.za -a 'dokku letsencrypt osf-case-management-prod'
```
