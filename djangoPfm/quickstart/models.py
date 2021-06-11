from django.db import models
from mongoengine import Document
from mongoengine.fields import (
   StringField,
   ObjectIdField,
)


#creating model here
class News(models.Model):
    meta={"collection","news"}
    title=models.CharField(max_length=32)
    content=models.TextField()
    #def __str__(self):
        #return self.title