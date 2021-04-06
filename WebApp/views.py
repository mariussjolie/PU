"""WebApp Views"""
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.forms import modelformset_factory, modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators import user_is_member_of_estate
from .forms import VoteForm, CommentForm, DistributeItemForm
from .models import Estate, Item, Vote, Notify, Comment


def home(request):
    """Home View"""
    estates = Estate.objects.filter(users__id=request.user.id)
    notifications = Notify.objects.filter(user_id=request.user.id)

    return render(request, 'WebApp/home.html', {'estates': estates, 'notifications': notifications})


@staff_member_required
def finish_estate(request, estate_id):
    """Finish Estate"""
    # Set estate to finished
    estate = Estate.objects.get(pk=estate_id)
    estate.is_finished = True
    estate.save()

    return redirect('estate', estate_id=estate_id)


@user_is_member_of_estate
def view_estate(request, estate_id):
    """Estate view"""
    estate = Estate.objects.get(pk=estate_id)
    Item.objects.filter(estate__id=estate_id)
    items = estate.item_set.all()

    if estate.is_finished:
        return render(request, 'WebApp/estate/estate_finished.html', {'estate': estate, 'items': items})

    VoteFormSet = modelformset_factory(Vote, form=VoteForm, extra=0)

    if request.method == 'POST':
        formset = VoteFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            # Delete notification if user has voted
            try:
                notification = Notify.objects.get(estate__id=estate_id, user__id=request.user.id)
                notification.delete()
            except Notify.DoesNotExist:
                pass
    else:
        votes = Vote.objects.filter(item__in=items, user=request.user)

        if not len(votes) == len(items):
            # Initiate votes for form
            for item in items:
                vote = Vote(user=request.user, item=item)
                try:
                    vote.save()
                except IntegrityError:  # Skip if already in DB
                    pass
            votes = Vote.objects.filter(item__in=items, user=request.user)

        formset = VoteFormSet(queryset=votes)

    return render(request, 'WebApp/estate/estate.html', {'estate': estate, 'items': items, 'formset': formset})


@staff_member_required
def admin_view_estate(request, estate_id):
    """Admin estate overview """
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.filter(is_staff=False)

    Item.objects.filter(estate__id=estate_id)
    items = estate.item_set.all()
    votes = {}

    for item in items:
        votes[item.id] = Vote.objects.filter(item__id=item.id)
        if len(votes.get(item.id)) == len(users):
            item.has_everyone_voted = True
            item.save()
        else:
            item.has_everyone_voted = False
            item.save()

    incomplete_items = Item.objects.filter(has_everyone_voted=False, estate_id=estate_id)
    completed_items = Item.objects.filter(has_everyone_voted=True, estate_id=estate_id)

    votes = Vote.objects.filter(item__in=items)

    return render(request, 'WebApp/estate/estate_admin.html',
                  {'estate': estate, 'incomplete_items': incomplete_items, 'completed_items': completed_items,
                   'users': users, 'votes': votes, 'items': items})


@staff_member_required
def admin_view_item(request, estate_id, item_id):
    """Item view for admin"""
    estate = Estate.objects.get(pk=estate_id)
    all_users = estate.users.all()
    item = Item.objects.get(pk=item_id)
    votes = Vote.objects.filter(item=item)
    normal_users = estate.users.filter(is_staff=False)

    notifications = Notify.objects.filter(estate__id=estate_id)
    comments = Comment.objects.filter(item__id=item_id)

    return render(request, 'WebApp/estate/item_admin.html', {'users': all_users, 'normal_users': normal_users,
                                                             'estate': estate, 'item': item, 'votes': votes,
                                                             'notifications': notifications,
                                                             'comments': comments})


@staff_member_required
def notify(request, estate_id, user_id, item_id):
    """Notify user to finish estate"""
    try:
        notification = Notify.objects.create(user_id=user_id, estate_id=estate_id)
        notification.save()
    except IntegrityError:
        pass

    return redirect("admin_view_estate_item", estate_id=estate_id, item_id=item_id)


@user_is_member_of_estate
def write_comment(request, item_id, estate_id):
    """Submit comment on item"""
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            estate = Estate.objects.get(id=estate_id)

            item = Item.objects.get(id=item_id)
            items = estate.item_set.all()

            if not item in items:
                raise PermissionDenied

            comment = form.save(commit=False)
            comment.user = request.user
            comment.item_id = item_id
            comment.save()
        else:
            raise PermissionDenied

    return redirect("show_item", estate_id=estate_id, item_id=item_id)


@user_is_member_of_estate
def show_item(request, estate_id, item_id):
    """Item view"""
    form = CommentForm()
    comments = Comment.objects.filter(item__id=item_id)
    item = Item.objects.get(id=item_id)

    return render(request, "WebApp/estate/item.html",
                  {"form": form, "estate_id": estate_id, "item": item, "comments": comments})


@user_is_member_of_estate
def estate_item_finished(request, estate_id, item_id):
    """Estate distribute item"""
    estate = Estate.objects.get(pk=estate_id)
    users = estate.users.filter(is_staff=False)
    item = Item.objects.get(pk=item_id)
    votes = Vote.objects.filter(item=item)

    ItemForm = modelform_factory(Item, form=DistributeItemForm)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse("estate_notfinished", args=[estate.id]))
    else:
        form = ItemForm(instance=item)
        form.fields["owner"].queryset = users

    return render(request, 'WebApp/estate/estate_item_finished.html', {'votes': votes, 'users': users, 'estate': estate,
                                                                       'item': item, 'form': form})


@staff_member_required
def admin_estate_notfinished(request, estate_id):
    """Estate distribute overview"""
    estate = Estate.objects.get(pk=estate_id)
    Item.objects.filter(estate__id=estate_id)

    items = estate.item_set.all()
    available_items = Item.objects.filter(estate_id=estate_id, owner=None)

    return render(request, 'WebApp/estate/estate_admin_notfinished.html', {'estate': estate, 'items': items,
                                                                           'available_items': available_items})
