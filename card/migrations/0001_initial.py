from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessCard",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(default="MIDEX", max_length=60),
                ),
                (
                    "tagline",
                    models.CharField(
                        default="Loss Adjusters and Surveyors", max_length=120
                    ),
                ),
                (
                    "rc_number",
                    models.CharField(
                        default="RC.442610",
                        max_length=40,
                        verbose_name="RC number",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        help_text="Leave empty to keep using the default MIDEX logo.",
                        null=True,
                        upload_to="card/",
                    ),
                ),
                (
                    "person_name",
                    models.CharField(default="Gbolade Otukoya", max_length=80),
                ),
                (
                    "credentials",
                    models.CharField(
                        default="AILA · CMEA · SBA",
                        help_text="Shown under the name, e.g. AILA · CMEA · SBA",
                        max_length=120,
                    ),
                ),
                (
                    "job_title",
                    models.CharField(default="MD/CEO", max_length=60),
                ),
                (
                    "phone_display",
                    models.CharField(
                        default="+234 813 930 6343",
                        help_text=(
                            "Used for Call and WhatsApp. Formatting (spaces) is "
                            "fine — digits are extracted automatically for the "
                            "tel: / wa.me / vCard links."
                        ),
                        max_length=30,
                        verbose_name="Phone (as shown on the card)",
                    ),
                ),
                (
                    "email_primary",
                    models.EmailField(
                        default="gotukoya@midexla.com",
                        help_text="Shown first on the card.",
                        max_length=254,
                        verbose_name="Primary email",
                    ),
                ),
                (
                    "email_secondary",
                    models.EmailField(
                        blank=True,
                        default="gotukoya@aol.com",
                        help_text="Shown second. Leave blank to show only one email.",
                        max_length=254,
                        verbose_name="Secondary email (optional)",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        default="Block 4 Unit 9, Lekki Paradise 1 Estate, Chevron, Lagos",
                        max_length=255,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Business card",
                "verbose_name_plural": "Business card",
            },
        ),
    ]
