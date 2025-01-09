from django.contrib import admin
from .models import OfferDetail, Offer


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
   
    list_display = ('title', 'user', 'offer_type', 'price', 'delivery_time_in_days')

  
    list_filter = ('offer_type', 'user')

    
    search_fields = ('title',)

 
    fieldsets = (
        (None, {
            'fields': ('title', 'user', 'offer_type', 'price')
        }),
        ('Details', {
            'fields': ('revisions', 'delivery_time_in_days', 'features')
        }),
    )

 
    list_per_page = 20


    ordering = ('-delivery_time_in_days',)



@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
 
    list_display = ('title', 'user', 'min_price', 'max_delivery_time', 'created_at', 'updated_at')


    list_filter = ('created_at', 'min_price', 'max_delivery_time')

 
    search_fields = ('title',)

 
    fieldsets = (
        (None, {
            'fields': ('title', 'user', 'description', 'image', 'min_price', 'max_delivery_time')
        }),
        ('Details', {
            'fields': ('details', 'user_details')
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )

    list_per_page = 20

    ordering = ('-created_at',)
