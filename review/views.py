from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from review.models import Review, Ticket
from . import forms, models


@login_required
def home(request):
    review = Review.objects.all()
    ticket = Ticket.objects.all()
    return render(request, 'review/home.html',
                  {'review': review,
                   'ticket': ticket})


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
