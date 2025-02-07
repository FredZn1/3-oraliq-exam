from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='detail'),
]
