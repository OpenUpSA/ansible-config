### Steps to deploy Munimoney
_____________________________

*for more detail see README of [OpenUpSA/ansible-config](https://github.com/OpenUpSA/ansible-config) repo's root
  - Run the following ansible-playbooks from root directory of the `OpenUpSA/ansible-config` repo
  - ensure you `pass git pull`
  - make use of appropriate inventory flag depending on environment and substitute out `staging` for correct `env_name` as necessary

1. Configure users of the new host*
   - `ansible-playbook -i inventory/staging.yml --limit munimoney users.yml --user root`
2. Configure dokku on the new host*
   - `ansible-playbook -i inventory/staging.yml --limit munimoney dokku-server.yml`
3. Cofigure mail server for forwarding cron errors on the new host*
   - `ansible-playbook -i inventory/staging.yml --limit munimoney ssmtp.yml -e "ssmtp_AuthUser=apikey ssmtp_AuthPass=$(pass show services/sendgrid.net | head -n 1) ssmtp_root=webapps@openup.org.za crond_MAILTO=webapps@openup.org.za"`
4. Deploy Dokku configuration*
   - `ansible-playbook -i inventory/staging.yml apps/munimoney/munimoney-web.yml` (use `--start-at-task "Dokku app exists"` if not first deploy)
   - Copy dokku git remote url to respective repo (see `Your dokku git remote` output of ansible playbook)
   e.g.: `git remote add dokku-staging dokku@staging.municipalmoney.gov.za:munimoney-staging-web` to [OpenUpSA/municipal-data](https://github.com/OpenUpSA/municipal-data)
5. Deploy to `web` by pushing master to dokku remote
   - For non-production, include for example: `dokku checks:disable munimoney-staging-web`
   - `git push dokku-staging master`
6. Setup Letsencrypt:
   - `dokku config:set --no-restart munimoney-staging-web DOKKU_LETSENCRYPT_EMAIL=webapps@openup.org.za`
   - `dokku letsencrypt munimoney-staging-web`
