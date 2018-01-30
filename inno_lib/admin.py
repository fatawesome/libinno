from django.contrib import admin
from .models import Document, Genre, Tag, Author, DocumentInstance

admin.site.register(Document)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(DocumentInstance)
