from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    # author = models.ManyToManyField(Author, help_text='select an author for this document')
    price = models.IntegerField(max_length=10)


class Author(models.Model):
    name = models.CharField(max_length=50)
    # document = models.ManyToManyField(Document, help_text='select a document written by this author')

    def __str__(self):
        return self.name
