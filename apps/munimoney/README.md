### Steps to deploy Munimoney
_____________________________

*for more detail see README of [OpenUpSA/ansible-config](https://github.com/OpenUpSA/ansible-config) repo's root
  - Run the following Ansible playbooks from root directory a local checkout of the `OpenUpSA/ansible-config` repo
  - ensure you `pass git pull`
  - make use of appropriate inventory flag depending on environment and substitute out `staging` for correct `env_name` as necessary

1. Configure users of the new host*
   - `ansible-playbook -i inventory/staging.yml --limit munimoney users.yml --user root`
2. Configure Dokku on the new host*
   - `ansible-playbook -i inventory/staging.yml --limit munimoney dokku-server.yml`
3. Configure mail server for forwarding cron errors on the new host*
   - `ansible-playbook -i inventory/staging.yml --limit munimoney ssmtp.yml -e "ssmtp_AuthUser=apikey ssmtp_AuthPass=$(pass show services/sendgrid.net | head -n 1) ssmtp_root=webapps@openup.org.za crond_MAILTO=webapps@openup.org.za"`
4. Deploy Dokku configuration*
   - `ansible-playbook -i inventory/staging.yml apps/munimoney/munimoney-web.yml` (use `--start-at-task "Dokku app exists"` if not first deploy)
   - Copy Dokku git remote url to respective repo (see `Your dokku git remote` output of Ansible playbook)
   e.g.: `git remote add dokku-staging dokku@staging.municipalmoney.gov.za:munimoney-staging-web` to local checkout of [OpenUpSA/municipal-data](https://github.com/OpenUpSA/municipal-data)
5. Deploy to `web` by pushing master to dokku remote
   - For non-production, include for example: `dokku checks:disable munimoney-staging-web` (from server)
   - `git push dokku-staging master` (from development machine)
6. Setup Letsencrypt (from server):
   - `dokku config:set --no-restart munimoney-staging-web DOKKU_LETSENCRYPT_EMAIL=webapps@openup.org.za`
   - `dokku letsencrypt munimoney-staging-web`
