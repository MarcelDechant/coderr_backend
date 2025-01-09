from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('title', 'customer_user', 'business_user', 'status', 'price', 'created_at', 'updated_at')

    list_filter = ('status', 'created_at')

    search_fields = ('title', 'status')


    fieldsets = (
        (None, {
            'fields': ('title', 'customer_user', 'business_user', 'status')
        }),
        ('Details', {
            'fields': ('revisions', 'delivery_time_in_days', 'price', 'offer_type', 'features')
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 20

    ordering = ('-created_at',)


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)