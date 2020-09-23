Procurement Portal
==================

Deployment

1. Install dokku-letsencrypt

    sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git

2. Run the playbook to configure the app

    ansible-playbook --tags app apps/procurement-portal/backend.yml

3. Add the git remote to your local clone (see the output from the playbook for the URI)

    git remote add dokku dokku@...hostname...:...app-name...

4. Enable letsencrypt for the app

    dokku letsnecrypt ...appname...

5. Enable letsnecrypt cron job

    dokku letsencrypt:cron-job --add ...appname...