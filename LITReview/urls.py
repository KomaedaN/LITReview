from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
import authentication.views
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', review.views.home, name='home'),
    path('ticket/upload/', review.views.ticket_upload, name='create_ticket'),
    path('review/upload/', review.views.review_upload, name='create_review'),
]
