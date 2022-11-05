from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from review.models import Review, Ticket


@login_required
def home(request):
    review = Review.objects.all()
    ticket = Ticket.objects.all()
    return render(request, 'review/home.html',
                  {'review': review,
                   'ticket': ticket})
