### Steps to deploy Gazettes-Aleph to production
________________________________________________

1. Run the following ansible-playbooks from root directory of `OpenUpSA/ansible-config` repo:
   - gazettes-aleph-web
   ```shell script
   ansible-playbook -i inventory/prod.yml apps/gazettes-aleph/gazettes-aleph-web.yml --start-at-task "Dokku app exists"
   ```
   - gazettes-aleph-worker
   ```shell script
   ansible-playbook -i inventory/prod.yml apps/gazettes-aleph/gazettes-aleph-worker.yml --start-at-task "Dokku app exists"
   ```
   In each case copy dokku remote url to respective repos (see `Your dokku git remote` output of ansible playbooks)
   e.g.:
     - `git remote add dokku dokku@hetzner1.openup.org.za:gazettes-aleph-prod-web` to `OpenUpSA/gazettes-aleph-dokku`
     - `git remote add dokku dokku@hetzner1.openup.org.za:gazettes-aleph-prod-worker` to `OpenUpSA/gazettes-aleph-dokku-worker`

2. ssh into instance where docker containers are going to be located
   - `dokku checks:disable gazettes-aleph-prod-worker`
   - `dokku proxy:disable gazettes-aleph-prod-worker`
   - `dokku docker-options:add gazettes-aleph-prod-worker deploy,run "-v /var/log/aleph-prod:/var/log"`
   - `dokku docker-options:add gazettes-aleph-prod-worker deploy,run "-v /var/lib/aleph-prod:/opt/aleph/data"`

3. Create Elasticsearch:1 app, [follow these docs](https://github.com/OpenUpSA/elasticsearch-0.90) for procedure,
   except sub in version 1 for 0.9. To summarize:
   1. `dokku apps:create elasticsearch-1`
   2. `dokku checks:disable elasticsearch-1`
   3. `dokku proxy:disable elasticsearch-1`
   4. `docker pull elasticsearch:1`
   5. `docker tag elasticsearch:1 dokku/elasticsearch-1:latest`
   6. `dokku config:set elasticsearch-1 ES_MIN_MEM=2g ES_MAX_MEM=4g`
   7. `dokku docker-options:add elasticsearch-1 deploy,run "-v /var/elasticsearch-1/data:/usr/share/elasticsearch/data"`
`  8. `dokku tags:deploy elasticsearch-1 latest`
   9. `dokku docker-options:add gazettes-aleph-prod-web deploy,run --link elasticsearch-1.web.1:elasticsearch`
   10. `dokku docker-options:add gazettes-aleph-prod-worker deploy,run --link elasticsearch-1.web.1:elasticsearch`
   11. `dokku config:set gazettes-aleph-prod-web ALEPH_ELASTICSEARCH_URI=http://elasticsearch:9200/`
   12. `dokku config:set gazettes-aleph-prod-worker ALEPH_ELASTICSEARCH_URI=http://elasticsearch:9200/`

4. Create Postgres database:
   1.
   ```shell script
   export DATABASE_IMAGE=postgres
   export DATABASE_IMAGE_VERSION=9.6.17
   dokku postgres:create gazettes-aleph
   ```   
   2. Link apps to databases:
      - `dokku postgres:link gazettes-aleph gazettes-aleph-prod-web`
      - `dokku postgres:link gazettes-aleph gazettes-aleph-prod-worker`
      - `dokku config:unset gazettes-aleph-prod-web DATABASE_URL`
      - `dokku config:unset gazettes-aleph-prod-worker DATABASE_URL`
      - `dokku config:set gazettes-aleph-prod-web ...`
      - `dokku config:set gazettes-aleph-prod-worker ...`
        
        Note, you can see what to paste in place of `...` by looking at the output of the link commands.
        In format: `ALEPH_DATABASE_URI=postgres://aleph:***@dokku-postgres-gazettes-aleph:5432/gazettes_aleph`

5. Deploy to each of `web` and `workers` by pushing master to dokku remote
   - `git push dokku master`

6. Dump and restore Postgres Database

```shell script
dokku postgres:import gazettes-aleph < /path/to/dump.postgrescustom
```

7. Index Elasticsearch:
   First enter gazettes-aleph-worker `dokku enter gazettes-aleph-prod-worker`, then
   - `aleph installdata`
   - `aleph resetindex`
   - `aleph index`



Tips and tricks:

To connect tp postgres DB:
  - `dokku postgres:connect gazettes-aleph`

To restart dokku app, e.g:
  - `dokku ps:restart gazettes-aleph-prod-worker`

To view web logs:
 - `dokku logs gazettes-aleph-prod-web -t`

To view celery logs (worker):
  - `tail -f less /var/log/aleph/celery.log`
