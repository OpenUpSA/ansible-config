# ElasticSearch based on elasticsearch:1 docker image

Not currently managed by ansible.

[Follow the docs for ES 0.90](https://github.com/OpenUpSA/elasticsearch-0.90)
for procedure, except sub in version 1 for 0.9. To summarize:

1. `dokku apps:create elasticsearch-1`
2. `dokku checks:disable elasticsearch-1`
3. `dokku proxy:disable elasticsearch-1`
4. `docker pull elasticsearch:1`
5. `docker tag elasticsearch:1 dokku/elasticsearch-1:latest`
6. `dokku config:set elasticsearch-1 ES_MIN_MEM=2g ES_MAX_MEM=4g` or as per needs of the app
    As a guideline, pombola for People's Assembly needed 8GB on ES 0.90, and still bombed out. PMG and Gazettes Aleph has run on 1GB on ES1 for years.
7. `dokku docker-options:add elasticsearch-1 deploy,run "-v /var/elasticsearch-1/data:/usr/share/elasticsearch/data"`
8. `dokku tags:deploy elasticsearch-1 latest`
