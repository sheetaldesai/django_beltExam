from django.conf.urls import include, url
from django.contrib import admin
from . import views

app_name = 'wishList'
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^wish_list/create/$', views.createWishList, name="createWishList"),
    url(r'^addWishList/$', views.addWishList, name="addWishList"),
    # url(r'^books/$', views.books, name="books"),
    # url(r'^books/add/$', views.bookAdd, name="bookAdd"),
    # url(r'^books/submitBook/$', views.submitBook, name="submitBook"),
    # url(r'^books/(?P<bookId>[0-9]+)/$', views.bookReviews, name="bookReviews"),
    # url(r'^users/(?P<userId>[0-9]+)/$', views.userDetails, name="userDetails"),
    # url(r'^books/(?P<bookId>[0-9]+)/addReview/$', views.addReview, name="addReview"),
    # url(r'^(?P<userId>[0-9]+)/edit/$', views.edit, name='edit'),
    # url(r'^/(?P<userId>[0-9]+)/delete/$', views.delete, name='delete')
    
]