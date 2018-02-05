from django.test import TestCase

from inno_lib.models.document_models import DocumentInstance, Book
from inno_lib.models.author import Author
from inno_lib.models.tag import Tag


class DocumentInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')
        Tag.objects.create(name='scary')
        Book.objects.create(title='book1', price=10, publisher='publisher1')
        Book.objects.get(id=1).authors.set([Author.objects.get(id=1)])
        Book.objects.get(id=1).tags.set([Tag.objects.get(id=1)])
        # Book.objects.get(id=1).edition.set(1)

    def setUp(self):
        DocumentInstance.objects.create(document=Book.objects.get(id=1), status='a')

    def test_document_in_instance_has_same_title(self):
        book = Book.objects.get(id=1)
        doc_inst = DocumentInstance.objects.all()[0]
        self.assertTrue(doc_inst.document.title == book.title)
