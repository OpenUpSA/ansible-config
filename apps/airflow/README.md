# airflow deployment

sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:enable airflow
dokku letsencrypt:cron-job --add
dokku ps:scale scheduler=1 triggerer=1