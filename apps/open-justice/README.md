Open Justice Aleph
==================

Install `ansible-role-docker`
----------------------------

```
ansible-galaxy install geerlingguy.docker
```

Post playbook
-------------
Start aleph in detached mode and set up tables

```
cd /var/open-justice/aleph
docker-compose up -d
docker-compose run --rm shell upgrade
sysctl -w vm.max_map_count=262144
```

To set up a user
----------------
Enter the Aleph shell:

```
make shell
```

Then:

```
aleph createuser --name="Alice" \
                 --admin \
                 --password=123abc \
                 user@example.com
```

Load sample data
---------------

```
aleph crawldir /aleph/contrib/testdata
```






