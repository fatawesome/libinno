from django.http import HttpResponse
from django.shortcuts import render

from .models import Document, Author, Genre, Tag, DocumentInstance


def index(request):
    """
    View function for home page of site.
    """
    num_docs = Document.objects.all().count()
    num_instances = DocumentInstance.objects.all().count()
    num_instances_available = DocumentInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    return render(
        request,
        'index.html',
        context={'num_docs': num_docs, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors},
    )
