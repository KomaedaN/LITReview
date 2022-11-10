from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
from itertools import chain
from django.db.models import CharField, Value
from authentication.models import UserFollows, User
from django.db import IntegrityError


@login_required
def home(request):
    review = models.Review.objects.all()
    ticket = models.Ticket.objects.all()
    return render(request, 'review/home.html', {'review': review, 'ticket': ticket})


@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def review_upload(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.POST['image']
            )
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form
    }
    return render(request, 'review/create_review.html', context=context)


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    user = request.user
    return render(request, 'review/view_ticket.html', {'ticket': ticket, 'user': user})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteContentForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_content' in request.POST:
            delete_form = forms.DeleteContentForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = home(request)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'feed.html', context={'posts': posts})


@login_required
def follow_users(request):
    subscriber = UserFollows.objects.filter(followed_user=request.user)
    all_follow = UserFollows.objects.filter(user=request.user)
    form = forms.FollowUsersForm()
    message = ''
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST['followed_user'])
                if request.user == followed_user:
                    message = 'Vous ne pouvez pas vous abonner'
                else:
                    try:
                        UserFollows.objects.create(user=request.user, followed_user=followed_user)
                        message = f'Vous suivez {followed_user}'

                    except IntegrityError:
                        message = f'Vous êtes déjà abonné à {followed_user}'

            except User.DoesNotExist:
                message = "L'utilisateur n'exsite pas"

    context = {
        'form': form,
        'message': message,
        'follows': all_follow,
        'subscriber': subscriber,
    }
    return render(request, 'review/subscription.html', context)


@login_required
def unfollow(request, user_follow_id):
    sub = get_object_or_404(UserFollows, id=user_follow_id)
    print(sub)
    unsub = forms.Unfollow()
    if request.method == 'POST':
        unsub = forms.DeleteContentForm(request.POST)
        if unsub.is_valid():
            sub.delete()
            return redirect('home')
    context = {
        'unsub': unsub,
    }
    return render(request, 'review/unfollow.html', context)
