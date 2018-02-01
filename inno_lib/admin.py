from django.contrib import admin
from .models import Document, Tag, Author, DocumentInstance

admin.site.register(Document)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(DocumentInstance)
