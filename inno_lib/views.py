from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import permission_required

from inno_lib.models.document_models import Document, DocumentInstance
from inno_lib.models.author import Author
from .forms import RenewDocumentForm

import datetime


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
    """
    Generic class-based view listing all documents in the system.
    """
    model = Document


class DocumentDetailView(generic.DetailView):
    """
    Generic class-based view the particular document page.
    """
    model = Document


class LoanedDocumentsByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing documents to the current user.
    """
    model = DocumentInstance
    template_name = 'inno_lib/documentinstance_list_borrowed_user.html'

    def get_queryset(self):
        return DocumentInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


@permission_required('inno_lib.can_mark_returned')
def renew_document_librarian(requset, pk):
    """
    Functional view describing the logic of renewing document instance by librarian.
    :param requset: HTTP request.
    :param pk: primary key for the DocumentInstance (truly, UUID).
    :return: rendered HTML.
    """
    docinst = get_object_or_404(DocumentInstance, pk=pk)

    # If this is a POST request then process the Form data
    if requset.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewDocumentForm(requset.POST)

        # Check if the form is valid:
        if form.is_valid():
            docinst.due_back = form.cleaned_data['renewal_date']
            docinst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewDocumentForm(initial={'renewal_date': proposed_renewal_date,})

    return render(requset, 'inno_lib/document_renew_librarian.html', {'form': form, 'docinst': docinst})


class BorrowedBooksForLibrarianListView(PermissionRequiredMixin, generic.ListView):
    """
    Genereic class-based view listing all borrowed documents to the librarian.
    """
    permission_required = 'inno_lib.can_mark_returned'
    model = DocumentInstance
    template_name = 'inno_lib/documentinstance_list_borrowed_librarian.html'

    def get_queryset(self):
        return DocumentInstance.objects.filter(status__exact='o').order_by('due_back')


def get_due_delta(user, document_instance):
    return datetime.timedelta(weeks=3)


def claim_document(request, pk):
    instance = DocumentInstance.objects.get(id=pk)

    if instance is None:
        raise ValueError('No document instance with id {}'.format(pk))

    if instance.status != 'a':
        raise ValueError('Document {} is not available for loan (has status {})'.format(pk, instance.status))

    instance.status = 'o'
    instance.borrower = request.user
    instance.due_back = datetime.date.today() + get_due_delta(request.user, instance)
    
    instance.save()

    # TODO: fix XSS
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# todo: this shouldn't be pushed
def return_document(request, pk):
    instance = DocumentInstance.objects.get(id=pk)

    if instance is None:
        raise ValueError('No document instance with id {}'.format(pk))

    if instance.status != 'o':
        raise ValueError('Document {} is not on loan (has status{})'.format(pk, instance.status))

    if instance.borrower.id != request.user.id:
        raise ValueError('Document {} is not borrowed by current user (current user id: {}, borrowed user id: {})'
                         .format(pk, request.user.id, instance.borrower.id))

    instance.status = 'a'
    instance.borrower = None
    instance.due_back = None

    instance.save()

    # TODO: fix XSS
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
