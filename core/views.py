from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.permissions import role_required
from .models import SiteSettings


@role_required("admin")
def logo_settings(request):
    obj = SiteSettings.get()
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "remove":
            if obj.logo:
                obj.logo.delete(save=False)
                obj.logo = None
                obj.save()
                messages.success(request, "Logo removed. Default logo will be shown.")
        else:
            if "logo" in request.FILES:
                if obj.logo:
                    obj.logo.delete(save=False)
                obj.logo = request.FILES["logo"]
                obj.save()
                messages.success(request, "Logo updated successfully!")
            site_name = request.POST.get("site_name", "").strip()
            tagline = request.POST.get("tagline", "").strip()
            if site_name:
                obj.site_name = site_name
            if tagline:
                obj.tagline = tagline
            obj.save()
            messages.success(request, "Settings saved.")
        return redirect("core:logo_settings")
    return render(request, "core/logo_settings.html", {"obj": obj})
