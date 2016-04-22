from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^users/login$', views.login, name='login'),
    
    url(r'^info/main$', views.show_info, name='show_info'),
    
    url(r'^lessons/main$', views.lessons_main, name='lessons_main'),
    url(r'^lessons/filter$', views.lessons_filter, name='lessons_filter'),
    url(r'^lessons/new$', views.lessons_new, name='lessons_new'),
    url(r'^lessons/create$', views.lessons_create, name='lessons_create'),
    url(r'^lessons/add_tag$', views.lessons_add_tag, name='lessons_add_tag'),
    url(r'^lessons/remove_tag$', views.lessons_remove_tag, name='lessons_remove_tag'),
    url(r'^lessons/edit$', views.lessons_edit, name='lessons_edit'),
    url(r'^lessons/update$', views.lessons_update, name='lessons_update'),

    url(r'^tags/main$', views.tags_main, name='tags_main'),
    url(r'^tags/filter$', views.tags_filter, name='tags_filter'),
    url(r'^tags/list$', views.tags_list, name='tags_list'),
]