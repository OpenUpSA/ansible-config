### Steps to deploy Salga Mobile API
____________________________________

The following steps assume that you have familiarized yourself with instructions of the README located at the
root of the [OpenUpSA/ansible-config](https://github.com/OpenUpSA/ansible-config) repo.

For commands below, ensure you make use of appropriate inventory flag depending on environment and substitute out
`prod` for correct `env_name` as necessary.

1. Confirm the following playbooks have already been run on target host before proceeding:
  - users.yml
  - dokku-server.yml
  - ssmtp.yml

2. Deploy Dokku configuration
   - `ansible-playbook -i inventory/prod.yml apps/salga-mobile-api/salga-mobile-api-web.yml` (use `--start-at-task "Dokku app exists"` if Dokku Daemon has already been configured on target host)
   - Copy Dokku git remote url to respective repo (see `Your dokku git remote` output of Ansible playbook)
   e.g.: `git remote add dokku-prod dokku@dokku9.code4sa.org:salga-mobile-api-prod-web` to local checkout of [OpenUpSA/salga-barometer-api](https://github.com/OpenUpSA/salga-barometer-api)
3. Deploy to `web` by pushing master to dokku remote
   - For non-production, include for example: `dokku checks:disable salga-mobile-api-prod-web` (from server)
   - `git push dokku-prod master` (from development machine)
4. Configure DNS with CNAME: `salga-mobile-api.openup.org.za` -> `dokku9.code4sa.org`
