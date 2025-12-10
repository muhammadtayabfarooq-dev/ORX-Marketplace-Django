from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("listings/new/", views.create_listing, name="create_listing"),
    path("listings/<slug:slug>/", views.listing_detail, name="listing_detail"),
    path("listings/<slug:slug>/edit/", views.edit_listing, name="edit_listing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("offers/<int:pk>/<str:status>/", views.update_offer_status, name="update_offer_status"),
    path("register/", views.register, name="register"),
]
