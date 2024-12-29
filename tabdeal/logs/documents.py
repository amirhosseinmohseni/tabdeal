from elasticsearch_dsl import Document, Date, Keyword, Text, connections, Integer, Boolean

connections.create_connection(hosts=["http://localhost:9200"], 
                              http_auth=('elastic', 'elastic_tabdeal'),
                              timeout=20)

class LogDocument(Document):
    level = Keyword()
    message = Text()
    timestamp = Date()
    type = Text()
    source = Text()
    destination = Text()
    amount = Integer()
    accept = Boolean()

    class Index:
        name = "logs"

    def save(self, **kwargs):
        return super().save(**kwargs)

LogDocument.init()