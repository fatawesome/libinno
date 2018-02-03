from django.db import models


class Tag(models.Model):
    """
    Model representing a Tag (e.g. 'funny', 'scary' etc.).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
