"""
Team seeding
"""

from django.db import migrations


def seed_teams(apps, schema_editor):
    """
    Docstring for seed_teams

    :param apps: Description
    :param schema_editor: Description
    """
    team = apps.get_model("core", "Team")

    teams = [
        {"id": 1, "name": "Patriots"},
        {"id": 2, "name": "Seahawks"},
    ]

    for t in teams:
        team.objects.update_or_create(
            id=t["id"],
            defaults={"name": t["name"]},
        )


class Migration(migrations.Migration):
    """
    Docstring for Migration
    """

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_teams, reverse_code=migrations.RunPython.noop),
    ]
