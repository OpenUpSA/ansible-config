### Steps to deploy Salga Mobile API
____________________________________

Ensure the server has been set up according to standard practise documented in the root of this repository

2. Deploy Dokku configuration
   - `ansible-playbook -i inventory/prod.yml apps/salga-mobile-api/salga-mobile-api-web.yml` (use `--start-at-task "Dokku app exists"` if Dokku Daemon has already been configured on target host)
   - Copy Dokku git remote url to respective repo (see `Your dokku git remote` output of Ansible playbook)
   e.g.: `git remote add dokku-prod dokku@dokku9.code4sa.org:salga-mobile-api-prod-web` to local checkout of [OpenUpSA/salga-barometer-api](https://github.com/OpenUpSA/salga-barometer-api)
3. Deploy to `web` by pushing master to dokku remote
   - For non-production, include for example: `dokku checks:disable salga-mobile-api-prod-web` (from server)
   - `git push dokku-prod master` (from development machine)
4. Configure DNS with CNAME: `salga-mobile-api.openup.org.za` -> `dokku9.code4sa.org`
