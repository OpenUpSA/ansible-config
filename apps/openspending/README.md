
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

Restore an elasticsearch backup to `/var/lib/dokku/data/storage/openspending-elasticsearch-{{ env_name }}` such that