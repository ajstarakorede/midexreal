from django.shortcuts import render
from django.utils.text import slugify

from .models import BusinessCard


def card_view(request):
    card = BusinessCard.load()

    filename = "-".join(
        filter(
            None,
            [
                slugify(card.company_name),
                slugify(card.person_name),
                "Business-Card",
            ],
        )
    )

    context = {
        "card": card,
        "pdf_filename": filename,
    }
    return render(request, "card/index.html", context)
