from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from inno_lib.models.document_models import Document, Book, DocumentInstance
from inno_lib.models.author import Author
from inno_lib.models.tag import Tag


class BorrowedBooksForLibrarianViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='test')
        Author.objects.create(first_name='test', last_name='test')
        Tag.objects.create(name='test')
        Book.objects.first().authors.set(Author.objects.all())
        Book.objects.first().tags.set(Tag.objects.all())
        User.objects.create_user(username='user1', email='test@test.com', password='test')
        User.objects.create_user(username='user2', email='test@test.com', password='test')
        Group.objects.create(name='Librarians')
        ct = ContentType.objects.create()
        Group.objects.create(name='Students')

    def setUp(self):
        test_book = Book.objects.first()
        self.book_inst = DocumentInstance.objects.create(document=test_book, status='a')
        self.user1 = User.objects.first()
        self.user2 = User.objects.all()[1]
        self.librarians_group = Group.objects.first()
        self.students_group = Group.objects.all()[1]

    # def test_librarian_can_see_borrowed_book(self):
    #     """
    #     Librarian must see on his page that user borrowed a book.
    #     Test-case 1.
    #     """
    #     self.user1.groups.add(self.librarians_group)
    #     self.user2.groups.add(self.students_group)
    #     self.user1.save()
    #     self.user2.save()
    #     self.client.login(username='user2', password='test')
    #
    #     book_inst = self.book_inst
    #     self.client.post(reverse('claim-document', kwargs={'pk': book_inst.id}))
    #     self.client.logout()
    #
    #     self.client.login(username='user1', password='test')
    #
    #     response = self.client.get(reverse('all-borrowed'))
    #
    #     self.assertEqual(response.status_code, 200)
