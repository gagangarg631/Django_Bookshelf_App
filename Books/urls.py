from django.urls import path,re_path
from . import views

from django.views.decorators.cache import cache_page

urlpatterns = [
    
    path('search', views.searchBook, name='search'),
    path('<slug:_category>', views.home, name='home'),
    # path('', cache_page(30)(views.home), name='home'),
    
    path('', views.home, name='home'),
    path('add-new-book/', views.addBook, name='add-book'),
    path('delete-book/<int:id>/', views.deleteBook, name='delete-book'),
    path('read/pdf/<int:id>/', views.showPdf, name='show-pdf'),
    path('pdf-closed/', views.pdfClosed, name='pdf-closed'),

    path('multiple-books/<slug:_action>/', views.handleMultipleBooks, name='handle-multiple'),

    re_path(r'^delete-multiple-books/((\d+)/)+$', views.deleteMultiple, name='delete-multiple'),
    re_path(r'^download-multiple-books/((\d+)/)+$', views.downloadMultiple, name='download-multiple'),
    re_path(r'share-multiple-books/(\d+)/((\d+)/)+$', views.shareMultiple, name='share-multiple'),

    # re_path(r'.*', views.pageNotExist, name='page-not-exist'),

    
]

 