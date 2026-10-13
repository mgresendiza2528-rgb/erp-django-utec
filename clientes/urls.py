from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.index, name='inicio'),
]