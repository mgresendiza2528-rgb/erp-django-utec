from django.urls import path
from django.http import HttpResponse

app_name = __name__.split('.')[0]


def inicio(request):
    return HttpResponse(
        "Modulo " + app_name + " - en construccion",
        content_type='text/html; charset=utf-8',
    )


urlpatterns = [
    path('', inicio, name='inicio'),
]