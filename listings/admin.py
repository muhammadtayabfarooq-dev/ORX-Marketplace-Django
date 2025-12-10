from django.contrib import admin

from .models import Category, Inquiry, Listing, Offer, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "status", "owner", "category", "created_at")
    list_filter = ("status", "category", "condition")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("listing", "offered_by", "amount", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("listing__title", "offered_by__username")


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("listing", "name", "email", "created_at")
    search_fields = ("listing__title", "name", "email")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "city")
