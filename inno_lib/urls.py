from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('document/<int:pk>', views.DocumentDetailView.as_view(), name='document-detail'),
    path('my/', views.LoanedDocumentsByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksForLibrarianListView.as_view(), name='all-borrowed'),
    path('document/<uuid:pk>/new/', views.renew_document_librarian, name='renew-document-librarian')
]
