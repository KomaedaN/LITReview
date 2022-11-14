from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
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
    path('ticket/<int:ticket_id>', review.views.view_ticket, name='view_ticket'),
    path('ticket/<int:ticket_id>/edit_ticket', review.views.edit_ticket, name='edit_ticket'),
    path('review/<int:ticket_id>/answer', review.views.answer_review, name='answer_review'),
    path('subscription/', review.views.follow_users, name='subscription'),
    path('subscription/unfollow', review.views.unfollow, name='unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
