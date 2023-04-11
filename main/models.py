from django.db import models
from accounts.models import MyUser as User
from services.mixin import DateMixin, SlugMixin
from services.generator import Generator


class Instagram(DateMixin, SlugMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    following = models.IntegerField(null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Instagram hesabi"
        verbose_name_plural = "Instagram hesablari"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Instagram)
        super(Instagram, self).save(*args, **kwargs)
