from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

from inno_lib.models.document_models import DocumentInstance, Document
from inno_lib.models.author import Author


class LoanedDocumentsByUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='test')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='test')
        test_user2.save()

        test_author = Author.objects.create(first_name='John', last_name='Doe')
        test_author.save()
        test_document = Document.objects.create(title='Test title')
        authors_for_document = Author.objects.all()
        test_document.authors.set(authors_for_document)
        test_document.save()

        num_of_doc_copies = 40
        for doc_copy in range(num_of_doc_copies):
            return_date = timezone.now() + datetime.timedelta(days=doc_copy % 5)
            if doc_copy % 2:
                borrower = test_user1
            else:
                borrower = test_user2
            status = 'm'
            DocumentInstance.objects.create(document=test_document,
                                            due_back=return_date, borrower=borrower, status=status)

    # TODO: it will not pass now, because there is no redirection implemented for this view.
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/accounts/login/?next=/my/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='test')
        resp = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'inno_lib/documentinstance_list_borrowed_user.html')

    def test_only_borrowed_documents_in_list(self):
        login = self.client.login(username='testuser1', password='test')
        resp = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('documentinstance_list' in resp.context)
        self.assertEqual(len(resp.context['documentinstance_list']), 0)

        get_ten_books = DocumentInstance.objects.all()[:10]

        for copy in get_ten_books:
            copy.status = 'o'
            copy.save()

        resp = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('documentinstance_list' in resp.context)

        for documentitem in resp.context['documentinstance_list']:
            self.assertEqual(resp.context['user'], documentitem.borrower)
            self.assertEqual('o', documentitem.status)
