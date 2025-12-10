from django import forms

from .models import Inquiry, Listing, Offer, UserProfile


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "category",
            "condition",
            "location",
            "image_url",
            "status",
        ]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["amount", "message"]

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Offer must be greater than zero.")
        return amount


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["name", "email", "message"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "city"]
