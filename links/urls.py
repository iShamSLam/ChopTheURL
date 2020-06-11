from django.urls import path

from . import views
# adding path to models
app_name = 'links'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.CreateView.as_view(), name='new'),
    path('<int:link_id>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.create_tiny_link, name='create'),
    path('links/<str:tiny_link>/', views.open_tiny_link, name='open'),
    path('delete/<int:link_id>/', views.delete_tiny_link, name='delete'),
]
