from django.db import models


# Create your models here.
class Book(models.Model):
  bid = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=50)
  author = models.CharField(max_length=50)
  category = models.CharField(max_length=50)
  pages = models.IntegerField()
  price = models.IntegerField()
  published_date = models.DateField()
  description = models.TextField()

"""
{
"bid":1,
"title":"aaa",
"author":"bbb",
"category":"programming",
"pages":100,
"price":20000,
"published_date":"2021-01-30",
"description":"ddddddd"
}
"""