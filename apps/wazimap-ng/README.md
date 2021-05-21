# Manual steps

After deploying the app:

## Configure Letsencrypt

    dokku letsencrypt:enable appname
    dokku letsencrypt:cron-job add appname

## Configure Redis

    dokku redis:create appname
    dokku redis:link appname appname