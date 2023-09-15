# Deployment


Run the `ocds-summary.yml` playbook to configure the dokku app on the server.

Note the git remote for the dokku app in the playbook output.

Delete the default domains from the app, leaving only the domain configured by the playbook.

```
dokku domains:remove vulekamali-ocds-summary-prod vulekamali-ocds-summary-prod.dokku.me vulekamali.gov.za
```

[Add the git remote to your local clone of the app repository, and push the master branch to the dokku git remote.](https://dokku.com/docs/deployment/application-deployment/#deploy-the-app)

Configure a notification email address for dokku-letsencrypt.

 dokku letsencrypt:set vulekamali-ocds-summary-prod email  team@yourdomain.gov.za

Enable letsencrypt to enable TLS and automatically renew certificates

```
dokku letsencrypt:enable vulekamali-budgetportal-prod
dokku letsencrypt:cron-job --add vulekamali-budgetportal-prod
```
