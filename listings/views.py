from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from .forms import InquiryForm, ListingForm, OfferForm, ProfileForm
from .models import Category, Listing, Offer


class HomeView(ListView):
    template_name = "listings/home.html"
    model = Listing
    context_object_name = "listings"
    paginate_by = 12

    def get_queryset(self):
        qs = Listing.objects.select_related("category", "owner").filter(status__in=["active", "reserved"])
        query = self.request.GET.get("q")
        category_slug = self.request.GET.get("category")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(location__icontains=query)
            )
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["query"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")
        return context


def listing_detail(request, slug):
    listing = get_object_or_404(Listing.objects.select_related("category", "owner"), slug=slug)
    offer_form = OfferForm()
    inquiry_form = InquiryForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "offer":
            if not request.user.is_authenticated:
                messages.info(request, "Please log in to make an offer.")
                return redirect(f"{reverse('login')}?next={listing.get_absolute_url()}")
            offer_form = OfferForm(request.POST)
            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                offer.listing = listing
                offer.offered_by = request.user
                offer.save()
                messages.success(request, "Offer submitted to the seller.")
                return redirect(listing.get_absolute_url())
        elif form_type == "inquiry":
            inquiry_form = InquiryForm(request.POST)
            if inquiry_form.is_valid():
                inquiry = inquiry_form.save(commit=False)
                inquiry.listing = listing
                if request.user.is_authenticated:
                    inquiry.sender = request.user
                    if not inquiry.name:
                        inquiry.name = request.user.get_full_name() or request.user.username
                    if not inquiry.email:
                        inquiry.email = request.user.email
                inquiry.save()
                messages.success(request, "Your question was sent to the seller.")
                return redirect(listing.get_absolute_url())

    return render(
        request,
        "listings/detail.html",
        {
            "listing": listing,
            "offer_form": offer_form,
            "inquiry_form": inquiry_form,
        },
    )


@login_required
def create_listing(request):
    form = ListingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        listing = form.save(commit=False)
        listing.owner = request.user
        listing.save()
        messages.success(request, "Listing created and published.")
        return redirect(listing.get_absolute_url())
    return render(request, "listings/form.html", {"form": form, "title": "New Listing"})


@login_required
def edit_listing(request, slug):
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    form = ListingForm(request.POST or None, instance=listing)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Listing updated.")
        return redirect(listing.get_absolute_url())
    return render(request, "listings/form.html", {"form": form, "title": "Edit Listing"})


@login_required
def dashboard(request):
    my_listings = Listing.objects.filter(owner=request.user).select_related("category")
    offers_for_me = Offer.objects.filter(listing__owner=request.user).select_related("listing", "offered_by")
    offers_made = Offer.objects.filter(offered_by=request.user).select_related("listing")
    profile_form = ProfileForm(request.POST or None, instance=request.user.profile)

    if request.method == "POST" and profile_form.is_valid():
        profile_form.save()
        messages.success(request, "Profile updated.")
        return redirect("dashboard")

    return render(
        request,
        "listings/dashboard.html",
        {
            "my_listings": my_listings,
            "offers_for_me": offers_for_me,
            "offers_made": offers_made,
            "profile_form": profile_form,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to ORX Marketplace.")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})


@login_required
def update_offer_status(request, pk, status):
    offer = get_object_or_404(Offer, pk=pk, listing__owner=request.user)
    if request.method == "POST" and status in dict(Offer.STATUS_CHOICES).keys():
        offer.status = status
        offer.save()
        messages.success(request, f"Offer marked as {offer.get_status_display()}.")
    return redirect("dashboard")
