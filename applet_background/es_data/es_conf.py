from elasticsearch import Elasticsearch

es_con = Elasticsearch(['116.63.150.180'], http_auth=('elastic', 'root001@'), timeout=3600)