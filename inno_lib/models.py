from django.db import models
from django.urls import reverse
import uuid


class Document(models.Model):
    """
    Model representing any Document in a system (but not a specific copy of one).
    """
    title = models.CharField(max_length=100)
    price = models.IntegerField
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
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class DocumentInstance(models.Model):
    """
    Model representing a specific copy of a Document (that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for this particular document")
    document = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Document availability')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.document.title)


class Genre(models.Model):
    """
    Model representing a Genre.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Model representing an Author
    """
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """
        :return: the url to access a particular Author.
        """
        return reverse('author-detail', args=str(self.id))

    def __str__(self):
        return '{0}, {1}'.format(self.first_name, self.last_name)


class Tag(models.Model):
    """
    Model representing a Tag (e.g. 'funny', 'scary' etc.).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
