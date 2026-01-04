from django.contrib import admin
from .models import Products, Cart, Order, Artisan, ArtisanRating
from django.utils.html import format_html


@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'display_image', 'created_at')
    search_fields = ('name', 'bio', 'address')
    readonly_fields = ('display_image',)
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'image', 'display_image', 'bio', 'address')
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No Image"

    display_image.short_description = 'Profile Image'


@admin.register(ArtisanRating)
class ArtisanRatingAdmin(admin.ModelAdmin):
    list_display = ('artisan', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('artisan__name', 'user__username', 'comment')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'display_artisan', 'display_image')
    list_filter = ('artisan',)
    search_fields = ('title', 'artisan__name')
    list_select_related = ('artisan',)

    def display_artisan(self, obj):
        if obj.artisan:
            return format_html('<a href="/admin/shop/artisan/{}/change/">{}</a>',
                               obj.artisan.id, obj.artisan.name)
        return "No Artisan"

    display_artisan.short_description = 'Artisan'

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image)
        return "No Image"

    display_image.short_description = 'Product Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'name', 'email', 'phone', 'city', 'state', 'total_price', 'payment_method', 'created_at')
    list_filter = ('created_at', 'payment_method')
    search_fields = ('user__username', 'name', 'phone')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__title')