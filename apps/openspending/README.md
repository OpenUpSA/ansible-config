
# Configure the kernel for elasticsearch

On the server

    echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf; sudo sysctl -p

# run the playbook

From your ansible controller (your laptop)

    --start-at-task "dokku_bot.ansible_dokku : dokku:plugin install"

# Enable the letsencrypt crontab

On the server:

    dokku letsencrypt:cron-job --add

# Restore an elasticsearch backup

Restore an elasticsearch backup to `/var/lib/dokku/data/storage/openspending-elasticsearch-{{ env_name }}` such that `ls /var/lib/dokku/data/storage/openspending-elasticsearch-prod` prints `nodes` if you are deploying to `prod`.

# Deploy apps:

Push https://github.com/vulekamali/dokku-elasticsearch-dockerfile to `openspending-elasticsearch-{{ env-name }}`

Push https://github.com/vulekamali/os-packager to `openspending-packager-{{ env-name }}`

Push https://github.com/vulekamali/os-conductor to `openspending-conductor-{{ env-name }}`

Push https://github.com/vulekamali/os-api to `openspending-api-{{ env-name }}`

Push https://github.com/vulekamali/os-admin to `openspending-admin-{{ env-name }}`

Push https://github.com/vulekamali/os-viewer to `openspending-viewer-{{ env_name }}`

Push https://github.com/vulekamali/os-explorer to `openspending-explorer-{{ env_name }}`

Push https://github.com/vulekamali/os-nginx-frontend to `openspending-frontend-{{ env_name }}`

With this, you should be able to log in at /packager and upload datasets.


# configure a repository for backups of the elasticsearch indexes

curl -XPUT 172.18.0.2:9200/_snapshot/s3_repository -H 'Content-Type: application/json' -d '
{
  "type": "s3",
  "settings": {
    "bucket": "vulekamali-openspending-elasticsearch-backups-prod",
    "region": "eu-west-1",
    "access_key": "the access key",
    "secret_key": "the secret key"
  }
}'

Monitor backup status by checking for "SUCCESS" at /elasticsearch-todays-backup