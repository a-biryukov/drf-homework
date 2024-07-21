from django.contrib import admin

from users.models import User, Payments


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'avatar', 'country',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid_course', 'paid_lesson', 'date_of_payment', 'payment_amount', 'payment_method')
