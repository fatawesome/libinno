from django.shortcuts import render
from django.views import generic

from inno_lib.models.document_models import Document, DocumentInstance
from inno_lib.models.author import Author


def index(request):
    """
    View function for home page of site.
    """
    num_docs = Document.objects.all().count()
    num_instances = DocumentInstance.objects.all().count()
    num_instances_available = DocumentInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Number of visit to this view, as counted in session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_docs': num_docs, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors, 'num_visits': num_visits},
    )


class DocumentListView(generic.ListView):
    model = Document


class DocumentDetailView(generic.DetailView):
    model = Document
