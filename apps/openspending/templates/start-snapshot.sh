set -euo pipefail

ip_address=`docker inspect -f '{% raw %}{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}{% endraw %}' openspending-elasticsearch-$1.web.1 |cut -c11-`

snapshot_name=`date +%Y-%m-%dt%H%M%S`

curl --fail -XPUT $ip_address:9200/_snapshot/s3_repository/$snapshot_name | grep --quiet '"accepted":true'
