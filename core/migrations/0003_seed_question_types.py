"""
Question Type seeding
"""

from django.db import migrations


def seed_question_types(apps, schema_editor):
    """
    Docstring for seed_question_types

    :param apps: Description
    :param schema_editor: Description
    """
    question_type = apps.get_model("core", "QuestionType")

    question_types = [
        {"id": 1, "type": "Team"},
        {"id": 2, "type": "Boolean"},
        {"id": 3, "type": "MultipleChoice"},
    ]

    for qt in question_types:
        question_type.objects.update_or_create(
            id=qt["id"],
            defaults={"type": qt["type"]},
        )


class Migration(migrations.Migration):
    """
    Docstring for Migration
    """

    dependencies = [
        ("core", "0002_seed_teams"),
    ]

    operations = [
        migrations.RunPython(
            seed_question_types, reverse_code=migrations.RunPython.noop
        ),
    ]
