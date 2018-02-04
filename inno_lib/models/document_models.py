from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid


class Document(models.Model):
    """
    Model representing any Document in a system (but not a specific copy of one).
    """
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    authors = models.ManyToManyField(
        'Author',
        help_text='Add authors for this book',
    )
    tags = models.ManyToManyField(
        'Tag',
        help_text='Add tags for this book',
    )

    def get_absolute_url(self):
        """
        :return: the url to access a particular Document instance.
        """
        return reverse('document-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    def display_authors(self):
        """
        Creates a string for the list of authors.
        :return: string of authors.
        """
        return ''.join([str(author) for author in self.authors.all()])

    def display_tags(self):
        """
        Creates a string for the list of tags
        :return: string of tags
        """
        return ''.join([tag.name for tag in self.tags.all()])

    def display_price(self):
        """
        :return: string representation of price.
        """
        return self.price


class Book(Document):
    """
    Model represents general book.
    """
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField


class Article(Document):
    editor = models.CharField(max_length=100)
    journal = models.CharField(max_length=100)


class DocumentInstance(models.Model):
    """
    Model representing a particular copy of the book (i. e. it can be borrowed from the library)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book for the whole lib')
    document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Document availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.id, self.document.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
