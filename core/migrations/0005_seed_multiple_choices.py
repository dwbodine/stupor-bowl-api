"""
Seed multiple choice options for questions.
"""

from django.db import migrations


def seed_multiple_choices(apps, schema_editor):
    """
    Docstring for seed_multiple_choices

    :param apps: Description
    """
    question = apps.get_model("core", "Question")
    question_type = apps.get_model("core", "QuestionType")
    multiple_choice = apps.get_model("core", "MultipleChoice")

    mc_type = question_type.objects.get(type="MultipleChoice")

    # Build a lookup of MC questions by ID (optional safety check)
    mc_question_ids = set(
        question.objects.filter(type=mc_type).values_list("id", flat=True)
    )

    # Define choices per Question ID
    # NOTE: Replace these with your real options.
    choices_by_question_id = {
        3: [
            ("Less than 5", 0),
            ("5 or more", 1),
        ],
        4: [
            ("Patriots", 0),
            ("Seahawks", 1),
            ("Neither one gets shown during the anthem", 2),
        ],
        10: [
            ("Not at all", 0),
            ("Less than 2", 1),
            ("2 or more", 2),
        ],
        12: [
            ("Heads", 0),
            ("Tails", 1),
        ],
        18: [
            ("Patriots", 0),
            ("Seahawks", 1),
            ("Neither", 2),
        ],
        19: [
            ("Less than 50", 0),
            ("50 or more", 1),
        ],
        20: [
            ("Less than 5", 0),
            ("5 or more", 1),
        ],
        21: [
            ("Red", 0),
            ("Blue", 1),
            ("Other", 2),
        ],
        22: [
            ("English", 0),
            ("Spanish", 1),
            ("Won't speak to the crowd", 2),
        ],
        23: [
            ("Less than 10", 0),
            ("10 or more", 1),
        ],
        28: [
            ("Less than 12 minutes", 0),
            ("12 minutes or more", 1),
        ],
        30: [
            ("Quarterback", 0),
            ("Running Back", 1),
            ("Wide Receiver", 2),
            ("Tight End", 3),
            ("Other Offensive player", 4),
            ("Somebody on defense", 5),
        ],
        32: [
            ("Less than 46 points", 0),
            ("46 points or more", 1),
        ],
        33: [
            ("Patriots", 0),
            ("Seahawks", 1),
            ("They both have the same", 2),
        ],
        34: [
            ("Green", 0),
            ("Orange", 1),
            ("Red", 2),
            ("Blue", 3),
            ("Other (or won't be shown on camera)", 4),
        ],
        35: [
            ("Team Fluff", 0),
            ("Team Ruff", 1),
        ],
    }

    # Create/update each choice row
    # Use a deterministic primary key scheme so this is idempotent
    # Example: id = question_id * 100 + order (supports up to 99 options per question)
    for question_id, options in choices_by_question_id.items():
        if question_id not in mc_question_ids:
            # Skip or raise; skipping is safer if your seed list is ahead/behind
            continue

        q = question.objects.get(pk=question_id)

        for choice_text, order in options:
            choice_id = question_id * 100 + order

            multiple_choice.objects.update_or_create(
                id=choice_id,
                defaults={
                    "question": q,
                    "choice": choice_text,
                    "order": order,
                },
            )


class Migration(migrations.Migration):
    """
    Docstring for Migration
    """

    dependencies = [
        ("core", "0004_seed_questions"),  # adjust to your actual filename/number
    ]

    operations = [
        migrations.RunPython(
            seed_multiple_choices, reverse_code=migrations.RunPython.noop
        ),
    ]
