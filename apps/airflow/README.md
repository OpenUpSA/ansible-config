# airflow deployment

Run the playbook


Set up letsencrypt

    sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
    dokku letsencrypt:enable airflow
    dokku letsencrypt:cron-job --add


Start scheduler and triggerer processes

    dokku ps:scale airflow scheduler=1 triggerer=1