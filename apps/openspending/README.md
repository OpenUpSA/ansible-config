
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

Push https://github.com/vulekamali/os-nginx-frontend to `openspending-frontend-{{ env_name }}`

With this, you should be able to log in at /packager and upload datasets.

You will not be able to visit / or follow links to the viewer from Admin until viewer and explorer are deployed.