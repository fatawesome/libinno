from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

from inno_lib.models.document_models import Book, DocumentInstance, Document
from inno_lib.models.author import Author

import datetime


class ClaimDocumentTest(TestCase):
    def setUp(self):
        self.group_faculty = Group(name='Faculty')
        self.group_faculty.save()
        self.group_students = Group(name='Students')
        self.group_students.save()
        self.user = User.objects.create_user(username='test', password='test', email='test@test.com')

        Author.objects.create(first_name='test', last_name='test')
        self.book = Book.objects.create(title='test', is_bestseller=True)
        self.book.authors.set(Author.objects.all())

    def test_borrowing_borrows(self):
        """
        Tests that view actually works.
        """
        self.user.groups.add(self.group_faculty)
        self.user.save()
        self.client.login(username='test', password='test')

        book_inst = DocumentInstance.objects.create(document=Book.objects.first(), status='a')
        response = self.client.post(reverse('claim-document', kwargs={'pk': book_inst.id}))
        book_inst = DocumentInstance.objects.first()

        self.assertEqual(book_inst.status, 'o')

    def test_faculty_checkout_book_4_weeks(self):
        """
        Faculty user should borrow book for 4 weeks.
        Test-case 4.
        """
        self.user.groups.add(self.group_faculty)
        self.user.save()
        self.client.login(username='test', password='test')

        book_inst = DocumentInstance.objects.create(document=Book.objects.first(), status='a')
        response = self.client.post(reverse('claim-document', kwargs={'pk': book_inst.id}))
        book_inst = DocumentInstance.objects.first()
        date = datetime.date.today()

        self.assertEqual(book_inst.due_back, date + datetime.timedelta(weeks=4))

    def test_stundent_checkout_bestseller_2_weeks(self):
        """
        Student user should borrow best-selling book for 2 weeks.
        Test-case 9
        """
        self.user.groups.add(self.group_students)
        self.user.save()
        self.client.login(username='test', password='test')

        book_inst = DocumentInstance.objects.create(document=Book.objects.first(), status='a')
        response = self.client.post(reverse('claim-document', kwargs={'pk': book_inst.id}))
        book_inst = DocumentInstance.objects.first()
        date = datetime.date.today()

        # self.assertTrue(book_inst.document.book.is_bestseller)
        self.assertEqual(book_inst.due_back, date + datetime.timedelta(weeks=2))
