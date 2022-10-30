# install [dokku-elasticsearch](https://github.com/dokku/dokku-elasticsearch)


# run

    echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf; sudo sysctl -p
    dokku elasticsearch:create openspending-prod

# run the playbook

# Run

    dokku elasticsearch:link openspending-prod openspending-api-prod