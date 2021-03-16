"""WebApp Views"""
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ItemForm, VoteForm
from .models import Estate, Item, Vote


def home(request):
    """Home View"""
    estates = Estate.objects.filter(users__id=request.user.id)
    return render(request, 'WebApp/home.html', {'estates': estates})


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
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.all()
    if not request.user in users:
        raise PermissionDenied

    Item.objects.filter(estate__id=estate_id)
    items = estate.item_set.all()
    votes = Vote.objects.filter(item__in=items)

    if not len(votes) == len(items):
        # Initiate votes for form
        for item in items:
            vote = Vote(user=request.user, item=item)
            try:
                vote.save()
            except IntegrityError:  # Skip if already in DB
                pass
        votes = Vote.objects.filter(item__in=items)

    VoteFormSet = modelformset_factory(Vote, form=VoteForm, extra=0)

    if request.method == 'POST':
        formset = VoteFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    else:
        formset = VoteFormSet(queryset=votes)

    return render(request, 'WebApp/estate/items.html', {'estate': estate, 'items': items, 'formset': formset})


def admin_view_estate(request, estate_id):
    """Admin overview """
    if not request.user.is_staff:
        raise PermissionDenied
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.all()

    Item.objects.filter(estate__id=estate_id)
    items = estate.item_set.all()
    votes = {}
    for item in items:
        votes[item.id] = Vote.objects.filter(item__id=item.id)
    votes = Vote.objects.filter(item__in=items)

    return render(request, 'WebApp/estate/items_admin.html',
                  {'estate': estate, 'items': items, 'votes': votes, 'users': users})


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
