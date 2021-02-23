"""WebApp Views"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from .forms import ItemForm
from .models import Estate, Item


def test_db(request):
    """TestDB view"""
    return render(request, 'WebApp/test_DB.html', {'estates': Estate.objects.all()})


def estate_overview(request):
    """Estate overview view"""
    user = request.user
    estates = Estate.objects.filter(users__id=user.id)
    return render(request, 'WebApp/estate/estates.html', {'estates': estates})


def view_estate(request, estate_id):
    """Estate view"""
    estate = Estate.objects.get(pk= estate_id)
    users = estate.users.all()
    if not request.user in users:
        raise PermissionDenied
    Item.objects.filter(estate__id= estate_id)
    items = estate.item_set.all()
    return render(request, 'WebApp/estate/items.html', {'estate': estate, 'items': items})


def item_image(request):
    """Item image view"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ItemForm()
    return render(request, 'WebApp/itemImage.html', {'form': form})


def success(request):
    """Success View"""
    return HttpResponse('successfully uploaded')
