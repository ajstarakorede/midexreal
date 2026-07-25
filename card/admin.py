from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import BusinessCard


@admin.register(BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("company_name", "tagline", "rc_number", "logo")}),
        (
            "Person",
            {"fields": ("person_name", "credentials", "job_title")},
        ),
        (
            "Contact",
            {
                "fields": (
                    "phone_display",
                    "email_primary",
                    "email_secondary",
                    "address",
                )
            },
        ),
    )
    readonly_fields = ("updated_at",)

    # There is only ever one record, so:
    # - never allow adding a second one
    def has_add_permission(self, request):
        return not BusinessCard.objects.exists()

    # - never allow deleting the only one
    def has_delete_permission(self, request, obj=None):
        return False

    # - skip the change-LIST screen entirely and go straight to the
    #   edit form, since a list of one row is just an extra click
    def changelist_view(self, request, extra_context=None):
        obj = BusinessCard.load()
        url = reverse(
            "admin:%s_%s_change"
            % (obj._meta.app_label, obj._meta.model_name),
            args=(obj.pk,),
        )
        return redirect(url)


admin.site.site_header = "MIDEX Admin"
admin.site.site_title = "MIDEX Admin"
admin.site.index_title = "Business card management"
