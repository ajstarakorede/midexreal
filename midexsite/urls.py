from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # The actual admin lives here.
    path("admin/", admin.site.urls),
    # Kept working as an alias, since it was asked for — redirects into
    # the same admin above. (Mounting admin.site.urls twice at two live
    # paths breaks Django's internal {% url %} link generation, so this
    # redirect is the safe way to make both addresses work.)
    path(
        "midex-django-admin/",
        RedirectView.as_view(url="/admin/", permanent=False),
    ),
    path("", include("card.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
