from django.test import TestCase
from django.urls import reverse

from inno_lib.models.document_models import Document
from inno_lib.models.author import Author
from inno_lib.models.tag import Tag


class DocumentListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')
        Tag.objects.create(name='scary')
        number_of_documents = 9
        for document_num in range(number_of_documents):
            Document.objects.create(title='Document %s' % document_num)
            Document.objects.get(id=document_num+1).authors.set([Author.objects.get(id=1)])
            Document.objects.get(id=document_num+1).tags.set([Tag.objects.get(id=1)])

    def test_view__url_exist_at_desired_location(self):
        resp = self.client.get('/documents/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('documents'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('documents'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inno_lib/document_list.html')

    def test_view_pagination_is_five(self):
        resp = self.client.get(reverse('documents'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['document_list']) == 5)

    def test_view_second_page_has_4_records(self):
        resp = self.client.get(reverse('documents')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['document_list']) == 4)
