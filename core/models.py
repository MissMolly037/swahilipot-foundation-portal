from django.db import models


class SiteSettings(models.Model):
    """Singleton model for portal-wide settings (logo, site name, etc.)"""
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    site_name = models.CharField(max_length=100, default="Swahilipot Hub Portal")
    tagline = models.CharField(max_length=200, default="Staff Portal")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
