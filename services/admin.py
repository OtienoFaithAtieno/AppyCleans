# Register your models here.
from django.contrib import admin
from .models import Service, Booking, Contact
from django.utils.html import format_html

admin.site.register(Service)
#admin.site.register(Booking)

@admin.register(Contact)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'service',
        'date',
        'time',
        'colored_status',
        'created_at'
    )

    list_filter = ('status', 'service', 'date')
    search_fields = ('user__username', 'email', 'phone')
    ordering = ('-created_at',)
  #  list_editable = ('status',)
  
    def colored_status(self, obj):
        color = {
            "pending": "orange",
            "confirmed": "blue",
            "completed": "green",
            "cancelled": "red",
        }.get(obj.status, "black")

        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            obj.status.capitalize()
        )

    colored_status.admin_order_field = 'status'
    colored_status.short_description = 'Status'
