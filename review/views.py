from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
from itertools import chain
from django.db.models import CharField, Value, Q
from authentication.models import UserFollows, User
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    ticket_id = []
    for i in reviews:
        review = i.ticket
        ticket_id.append(review)
    tickets = get_users_viewable_tickets(request)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'review/feed.html', {'posts': posts, 'ticket_id': ticket_id})


@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def review_upload(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
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
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    user = request.user
    return render(request, 'review/view_review.html', {'review': review, 'user': user})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteContentForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('feed')
        if 'delete_content' in request.POST:
            delete_form = forms.DeleteContentForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('feed')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteContentForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, request.FILES, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('feed')
        if 'delete_content' in request.POST:
            delete_form = forms.DeleteContentForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('feed')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_review.html', context=context)


@login_required
def answer_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')

    context = {
        'ticket': ticket,
        'review_form': review_form,
    }
    return render(request, 'review/answer_review.html', context=context)


@login_required
def follow_users(request):
    unsub = forms.Unfollow()
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
        'unsub': unsub,
    }
    return render(request, 'review/subscription.html', context)


@login_required
def unfollow(request):
    sub = get_object_or_404(UserFollows, id=request.POST["user_followed_id"])
    unsub = forms.Unfollow()
    if request.method == 'POST':
        unsub = forms.Unfollow(request.POST)
        if 'user_followed_id' in request.POST:
            if unsub.is_valid():
                sub.delete()
                return redirect('subscription')

    context = {
        'unsub': unsub,
    }
    return redirect('subscription')


@login_required
def get_users_viewable_reviews(request):
    user = request.user
    all_follows = user_follow(request)
    all_reviews = models.Review.objects.filter(user__in=all_follows).distinct()
    return all_reviews


@login_required
def get_users_viewable_tickets(request):
    user = request.user
    all_follows = user_follow(request)
    tickets = models.Ticket.objects.filter(user__in=all_follows)
    return tickets


@login_required
def user_follow(request):
    user = request.user
    user_follow = UserFollows.objects.filter(user=user)
    all_follows = []
    for follow in user_follow:
        all_follows.append(follow.followed_user)
    all_follows.append(user)
    return all_follows
