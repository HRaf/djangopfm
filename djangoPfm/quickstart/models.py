from django.db import models


#creating model here
class News(models.Model):
    meta={"collection","news"}
    url = models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    content=models.TextField()
    datePost =models.TextField()
    language = models.CharField(default='arabic',max_length=100)
    classe = models.IntegerField()

