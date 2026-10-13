from django.shortcuts import render


def index(request):
    app = __name__.split('.')[0]
    context = {'titulo': app.capitalize()}
    return render(request, app + '/index.html', context)