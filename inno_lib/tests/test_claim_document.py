from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
import uuid

from inno_lib.models.document_models import DocumentInstance, Document
from inno_lib.models.author import Author


class ClaimDocumentTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='test')
        test_user1.save()

        test_author = Author.objects.create(first_name='John', last_name='Doe')
        test_author.save()
        test_document = Document.objects.create(title='Test title')
        authors_for_document = Author.objects.all()
        test_document.authors.set(authors_for_document)
        test_document.save()

        DocumentInstance.objects.create(document=test_document, status='a')

    def test_borrowing_redirects(self):
        login = self.client.login(username='testuser1', password='test')
        test_uid = DocumentInstance.objects.first().id
        resp = self.client.post(reverse('claim-document', kwargs={'pk': test_uid, }))
        self.assertEqual(resp.status_code, 302)

    def test_borrowing_borrows(self):
        doc_inst = DocumentInstance.objects.first()
        login = self.client.login(username='testuser1', password='test')
        test_uid = doc_inst.id
        resp = self.client.post(reverse('claim-document', kwargs={'pk': test_uid, }))
        doc_inst = DocumentInstance.objects.first()

        self.assertEqual(doc_inst.status, 'o')





