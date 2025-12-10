from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Listing(models.Model):
    CONDITION_CHOICES = [
        ("new", "New / Unused"),
        ("like_new", "Like New"),
        ("good", "Good"),
        ("fair", "Fair"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("reserved", "Reserved"),
        ("sold", "Sold"),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name="listings", on_delete=models.PROTECT)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="good")
    location = models.CharField(max_length=120)
    image_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    owner = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("listing_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Listing.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class Offer(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    listing = models.ForeignKey(Listing, related_name="offers", on_delete=models.CASCADE)
    offered_by = models.ForeignKey(User, related_name="offers_made", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Offer {self.amount} on {self.listing}"


class Inquiry(models.Model):
    listing = models.ForeignKey(Listing, related_name="inquiries", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="inquiries", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Inquiry for {self.listing}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=120, blank=True)

    def __str__(self) -> str:
        return f"Profile for {self.user.username}"
