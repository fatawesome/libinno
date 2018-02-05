from django.contrib import admin
from inno_lib.models.document_models import Document, DocumentInstance, Book, Article
from inno_lib.models.author import Author
from inno_lib.models.tag import Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


class DocumentInstanceInline(admin.TabularInline):
    model = DocumentInstance


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_price', 'display_authors', 'display_tags')
    inlines = [DocumentInstanceInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentInstance)
class DocumentInstanceAdmin(admin.ModelAdmin):
    list_display = ('document', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('document', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'borrower', 'due_back')
        })
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
