"""WebApp Views"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory, modelform_factory
from django.db import IntegrityError


from .forms import ItemForm, VoteForm, DistributeItemForm
from .models import Estate, Item, Vote, Notify


def home(request):
    """Home View"""
    estates = Estate.objects.filter(users__id=request.user.id)
    notifications = Notify.objects.filter(user_id=request.user.id)

    return render(request, 'WebApp/home.html', {'estates': estates, 'notifications': notifications})


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
    votes = Vote.objects.filter(item__in=items, user=request.user)

    if not len(votes) == len(items):
        # Initiate votes for form
        for item in items:
            vote = Vote(user=request.user, item=item)
            try:
                vote.save()
            except IntegrityError:  # Skip if already in DB
                pass
        votes = Vote.objects.filter(item__in=items,user=request.user)

    VoteFormSet = modelformset_factory(Vote, form=VoteForm, extra=0)

    if request.method == 'POST':
        formset = VoteFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            try:
                notification = Notify.objects.get(estate__id=estate_id, user__id=request.user.id)
                notification.delete()
            except Notify.DoesNotExist:
                pass
    else:
        formset = VoteFormSet(queryset=votes)

    return render(request, 'WebApp/estate/items.html', {'estate': estate, 'items': items, 'formset': formset})


def admin_view_estate(request, estate_id):
    """Admin overview """
    if not request.user.is_staff:
        raise PermissionDenied
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.all()

    notifications = Notify.objects.filter(estate__id=estate_id)

    Item.objects.filter(estate__id=estate_id)
    items = estate.item_set.all()
    votes = {}
    for item in items:
        votes[item.id] = Vote.objects.filter(item__id=item.id)
    votes = Vote.objects.filter(item__in=items)

    return render(request, 'WebApp/estate/items_admin.html',
                  {'estate': estate, 'items': items, 'votes': votes, 'users': users, 'notifications': notifications})


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


def notify(request, estate_id, user_id):
    if not request.user.is_staff:
        raise PermissionDenied
    try:
        notifcation = Notify.objects.create(user_id=user_id, estate_id=estate_id)
        notifcation.save()
    except IntegrityError:
        pass

    return redirect("estate.adminoverview", estate_id=estate_id)


def status(request, estate_id):
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.all()
    if not request.user in users:
        raise PermissionDenied
    return render(request, 'WebApp/admin/status.html', {'users': users, 'estate': estate})


def estate_item_finished(request, estate_id, item_id):
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.all()
    item = Item.objects.get(pk=item_id)
    votes = Vote.objects.filter(item=item)
    if not request.user in users:
        raise PermissionDenied

    ItemForm = modelform_factory(Item, form=DistributeItemForm)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse("estate_notfinished", args=[estate.id]))
    else:
        form = ItemForm(instance=item)

    return render(request, 'WebApp/estate/estate_item_finished.html', {'votes': votes, 'users': users, 'estate': estate,
                                                            'item': item, 'form': form})


def estate_notfinished(request, estate_id):
    """Estate view"""
    estate = Estate.objects.get(pk= estate_id)
    users = estate.users.all()
    if not request.user in users:
        raise PermissionDenied

    Item.objects.filter(estate__id= estate_id)
    items = estate.item_set.all()

    return render(request, 'WebApp/estate/estate_notfinished.html', {'estate': estate, 'items': items})


def estate_finished(request, estate_id):
    """Estate view"""
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.all()
    if not request.user in users:
        raise PermissionDenied

    Item.objects.filter(estate__id=estate_id)
    items = estate.item_set.all()

    estate.is_finished = True
    estate.save()

    return render(request, 'WebApp/estate/estate_finished.html', {'estate': estate, 'items': items})