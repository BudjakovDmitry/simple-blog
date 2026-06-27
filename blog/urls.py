from django.urls import path

from . import views


urlpatterns = [
    path("", views.feed, name="feed"),
    path("linux", views.linux, name="linux"),
    path("html", views.html, name="html"),
    path("page/<int:page>/", views.page, name="page"),
    path("articles/<str:slug>/", views.read, name="read"),
]
