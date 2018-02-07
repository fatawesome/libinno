from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from inno_lib.models.document_models import Document, Book, DocumentInstance
from inno_lib.models.author import Author
from inno_lib.models.tag import Tag


class DocumentDetailViewTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='test', last_name='test')
        self.faculty_group = Group.objects.create(name='Faculty')
        self.students_group = Group.objects.create(name='Students')
        self.librarians_group = Group.objects.create(name='Librarians')
        Book.objects.create(title='test')
        Book.objects.first().authors.set(Author.objects.all())

        self.book_inst1 = DocumentInstance.objects.create(document=Book.objects.first(), status='a')
        self.book_inst2 = DocumentInstance.objects.create(document=Book.objects.first(), status='a')

        self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='user1')
        self.user1.groups.add(self.students_group)
        self.user1.save()
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='user2')
        self.user2.groups.add(self.students_group)
        self.user1.save()
        self.user3 = User.objects.create_user(username='user3', email='user3@test.com', password='user3')
        self.user3.groups.add(self.faculty_group)


    # def test_three_try_to_borrow_book(self):
    #     self.client.login(username='user1', password='user1')
    #     self.client.login(user)

