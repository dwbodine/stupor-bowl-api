"""
Appsettings seeding
"""

from django.db import migrations


def seed_appsettings(apps, schema_editor):
    """
    Docstring for seed_appsettings

    :param apps: Description
    :param schema_editor: Description
    """
    setting = apps.get_model("core", "AppSettings")

    settings = [
        {"id": 1, "registration_open": "True", "results_published": "False"},
    ]

    for s in settings:
        setting.objects.update_or_create(
            id=s["id"],
            defaults={
                "registration_open": s["registration_open"],
                "results_published": s["results_published"],
            },
        )


class Migration(migrations.Migration):
    """
    Docstring for Migration
    """

    dependencies = [
        ("core", "0005_seed_multiple_choices"),
    ]

    operations = [
        migrations.RunPython(seed_appsettings, reverse_code=migrations.RunPython.noop),
    ]
