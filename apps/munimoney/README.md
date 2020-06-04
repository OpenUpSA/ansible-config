### Steps to deploy Munimoney
_____________________________

* for more detail see README of `OpenUpSA/ansible-config` repo's root
  - ensure you `pass git pull`
  - make use of appropriate inventory flag depending on environment and substitute out `sandbox` for correct `env_name` as necessary

1. Configure users of the new host*
   `ansible-playbook --limit munimoney users.yml --user root`
2. Configure dokku on the new host*
   `ansible-playbook --limit munimoney dokku-server.yml`
3. Cofigure mail server for forwarding cron errors on the new host*
   `ansible-playbook --limit munimoney ssmtp.yml -e "ssmtp_AuthUser=apikey ssmtp_AuthPass=$(pass show services/sendgrid.net | head -n 1) ssmtp_root=webapps@openup.org.za crond_MAILTO=webapps@openup.org.za"`
4. Run the following ansible-playbooks from root directory of `OpenUpSA/ansible-config` repo:
   `ansible-playbook -i inventory/sandbox.yml apps/munimoney/munimoney-web.yml` (use `--start-at-task "Dokku app exists"` if not first deploy)
   Copy dokku git remote url to respective repo (see `Your dokku git remote` output of ansible playbook)
   e.g.:
     - `git remote add dokku-sandbox dokku@munimoney1-hetzner.openup.org.za:munimoney-sandbox-web` to `OpenUpSA/municipal-data`

5. Deploy to `web` by pushing master to dokku remote
   - `git push dokku-sandbox master`
