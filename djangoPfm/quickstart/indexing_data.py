import elasticsearch
from elasticsearch_dsl import Search
import pathlib


def add_data_to_elastic(title, content, date):
    INDEX_NAME = 'news-index'

    ELASTIC_HOST = 'http://localhost:9200/'

    client = elasticsearch.Elasticsearch(hosts=[ELASTIC_HOST])

    data_1 = {
        'title': title,
        'body': content,
        'date': date,
    }

    client.index(index=INDEX_NAME, body=data_1)
