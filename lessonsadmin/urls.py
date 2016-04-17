from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/main$', views.show_info, name='show_info'),
    url(r'^lessons/main$', views.lessons_main, name='lessons_main'),
    url(r'^lessons/filter$', views.lessons_filter, name='lessons_filter'),
    url(r'^lessons/new$', views.lessons_new, name='lessons_new'),
    url(r'^lessons/create$', views.lessons_create, name='lessons_create'),
]