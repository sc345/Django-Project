from django.urls import path
from .import views
app_name ='post'
urlpatterns = [

    path('index/',views.post_index, name='index'),
    path('create/',views.post_create, name='create'),
    path('<slug>/',views.post_detail, name='detail'),
    path('<slug>/update/',views.post_update, name='update'),
    path('<slug>/delete/',views.post_delete, name='delete'),

  ]
