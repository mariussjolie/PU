from django.shortcuts import render

from .models import Estate


def TestDB(request):
    return render(request, 'WebApp/test_DB.html', {'estates': Estate.objects.all()})
