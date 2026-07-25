import re

from django.db import models


class BusinessCard(models.Model):
    """
    Singleton model: there is only ever ONE row (pk=1).
    Whatever the admin edits here is what renders on the live site
    AND is what gets baked into the downloadable PDF, because both
    read from this same record every time the page loads.
    """

    # --- Brand ---
    company_name = models.CharField(max_length=60, default="MIDEX")
    tagline = models.CharField(
        max_length=120, default="Loss Adjusters and Surveyors"
    )
    rc_number = models.CharField(
        max_length=40, default="RC.442610", verbose_name="RC number"
    )
    logo = models.ImageField(
        upload_to="card/",
        blank=True,
        null=True,
        help_text="Leave empty to keep using the default MIDEX logo.",
    )

    # --- Person ---
    person_name = models.CharField(max_length=80, default="Gbolade Otukoya")
    credentials = models.CharField(
        max_length=120,
        default="AILA · CMEA · SBA",
        help_text="Shown under the name, e.g. AILA · CMEA · SBA",
    )
    job_title = models.CharField(max_length=60, default="MD/CEO")

    # --- Contact ---
    phone_display = models.CharField(
        max_length=30,
        default="+234 813 930 6343",
        verbose_name="Phone (as shown on the card)",
        help_text="Used for Call and WhatsApp. Formatting (spaces) is fine — "
        "digits are extracted automatically for the tel: / wa.me / vCard links.",
    )
    email_primary = models.EmailField(
        default="gotukoya@midexla.com",
        verbose_name="Primary email",
        help_text="Shown first on the card.",
    )
    email_secondary = models.EmailField(
        blank=True,
        default="gotukoya@aol.com",
        verbose_name="Secondary email (optional)",
        help_text="Shown second. Leave blank to show only one email.",
    )
    address = models.CharField(
        max_length=255,
        default="Block 4 Unit 9, Lekki Paradise 1 Estate, Chevron, Lagos",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business card"
        verbose_name_plural = "Business card"

    def __str__(self):
        return f"{self.company_name} card — {self.person_name}"

    # ----- Singleton plumbing -----
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # the single record is never deletable from the admin

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    # ----- Derived values used for tel: / wa.me / vCard -----
    @property
    def phone_digits(self):
        """Digits only, no plus — e.g. 2348139306343. Used for wa.me links."""
        return re.sub(r"\D", "", self.phone_display)

    @property
    def phone_e164(self):
        """+ plus digits — e.g. +2348139306343. Used for tel: and the vCard."""
        return "+" + self.phone_digits
