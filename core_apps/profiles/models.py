from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = (
            "M",
            _("Male"),
        )
        FEMALE = (
            "F",
            _("Female"),
        )
        OTHER = (
            "O",
            _("Other"),
        )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), max_length=30, default="+84123456789"
    )
    about_me = models.TextField(
        verbose_name=_("about me"), default="Say something about yourself."
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=24,
    )
    country = CountryField(
        verbose_name=_("country"),
        default="VN",
        blank=False,
        null=False,
    )
    city = models.CharField(
        verbose_name=_("city"),
        default="HCM City",
        max_length=180,
        blank=False,
        null=False,
    )
    profile_photo = models.ImageField(
        verbose_name=_("profile phooto"),
        default="/profile_default.png",
    )
    twitter = models.CharField(
        verbose_name=_("twitter handle"), max_length=180, blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def __str__(self):
        return f"{self.user.first_name}'s Profile"  # type: ignore

    def follow(self, profile):
        self.followers.add(profile)

    def unfollower(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        self.followers.filter(pkid=profile.pkid).exists()
