### Steps to deploy Munimoney
_____________________________

The following steps assume that you have familiarized yourself with instructions of the README located at the
root of the [OpenUpSA/ansible-config](https://github.com/OpenUpSA/ansible-config) repo.

For commands below, ensure you make use of appropriate inventory flag depending on environment and substitute out
`staging` for correct `env_name` as necessary.

1. Confirm the following playbooks have already been run on target host before proceeding:
  - users.yml
  - dokku-server.yml
  - ssmtp.yml

2. Deploy Dokku configuration
   - `ansible-playbook -i inventory/staging.yml apps/munimoney/munimoney-web.yml` (use `--start-at-task "Dokku app exists"` if Dokku Daemon has already been configured on target host)
   - Copy Dokku git remote url to respective repo (see `Your dokku git remote` output of Ansible playbook)
   e.g.: `git remote add dokku-staging dokku@staging.municipalmoney.gov.za:munimoney-staging-web` to local checkout of [OpenUpSA/municipal-data](https://github.com/OpenUpSA/municipal-data)
3. Deploy to `web` by pushing master to dokku remote
   - For non-production, include for example: `dokku checks:disable munimoney-staging-web` (from server)
   - `git push dokku-staging master` (from development machine)
4. Assuming DNS is correctly setup, run Letsencrypt command (from server):
   - `dokku letsencrypt munimoney-staging-web`
