from django.contrib import admin
from review.models import Review, Ticket


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'user', 'rating')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)