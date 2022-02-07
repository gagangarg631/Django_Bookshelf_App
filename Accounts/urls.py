from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('books/',include('Books.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    # re_path(r'.*', views.pageNotExist, name='page-not-exist'),
]