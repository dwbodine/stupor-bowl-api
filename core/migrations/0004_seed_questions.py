"""
Docstring for core.migrations.0004_seed_questions
"""

from django.db import migrations


def seed_questions(apps, schema_editor):
    """
    Docstring for seed_questions

    :param apps: Description
    :param schema_editor: Description
    """
    question = apps.get_model("core", "Question")
    question_type = apps.get_model("core", "QuestionType")

    # Fetch required QuestionTypes
    team_type = question_type.objects.get(type="Team")
    boolean_type = question_type.objects.get(type="Boolean")
    multiple_choice_type = question_type.objects.get(type="MultipleChoice")

    questions = [
        {
            "id": 1,
            "question": "Will Charlie Puth mess up a word in the National Anthem?",
            "points": 5,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 2,
            "question": "Will the National Anthem be over in less than 2:05?",
            "points": 15,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 3,
            "question": "Length of the final word " "Brave" " in seconds?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 4,
            "question": "Which coach gets shown first during the Anthem?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 5,
            "question": "Will Jon Hamm be shown on camera at the game (after 6 PM EST / 3 PM PST)?",
            "points": 5,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 6,
            "question": "Will Post Malone be shown on camera at the game (after 6 PM EST / 3 PM PST)?",
            "points": 5,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 7,
            "question": "Will Mark Wahlberg be shown on camera at the game (after 6 PM EST / 3 PM PST)?",
            "points": 5,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 8,
            "question": "Will Chris Pratt be shown on camera at the game (after 6 PM EST / 3 PM PST)?",
            "points": 5,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 9,
            "question": "Will the Golden Gate Bridge in San Francisco be shown on TV between 6 PM EST (3 PM PST) and kickoff?",
            "points": 15,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 10,
            "question": "How many times will Taylor Swift be shown on TV between kickoff and halftime?",
            "points": 25,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 11,
            "question": "Will the game start within 5 minutes of 6:30 PM EST / 3:30 PM PST (i.e., between 6:25 - 6:35 PM)?",
            "points": 20,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 12,
            "question": "Will the coin toss be heads or tails?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 13,
            "question": "Who wins the coin toss?",
            "points": 5,
            "default_answer": 0,
            "type": team_type,
        },
        {
            "id": 14,
            "question": "Who will kick off first?",
            "points": 5,
            "default_answer": 0,
            "type": team_type,
        },
        {
            "id": 15,
            "question": "Who will score first?",
            "points": 5,
            "default_answer": 0,
            "type": team_type,
        },
        {
            "id": 16,
            "question": "Who will score a TD first?",
            "points": 5,
            "default_answer": 0,
            "type": team_type,
        },
        {
            "id": 17,
            "question": "Which kicker will score first (FG or extra point)?",
            "points": 2,
            "default_answer": 0,
            "type": team_type,
        },
        {
            "id": 18,
            "question": "Who will throw an interception first?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 19,
            "question": "How many commercials between kickoff and the halftime show?",
            "points": 25,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 20,
            "question": "How many of those will be car commercials?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 21,
            "question": "Color of the first Doritos bag in commercials?",
            "points": 15,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 22,
            "question": "Halftime Show: Will Bad Bunny speak to the crowd first in English or Spanish?",
            "points": 15,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 23,
            "question": "Halftime Show: Total number of songs in the halftime show (including partial songs)?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 24,
            "question": "Halftime Show: Will Bad Bunny perform "
            "Baile Inolvidable"
            "?",
            "points": 5,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 25,
            "question": "Halftime Show: Will Cardi B make a guest appearance?",
            "points": 15,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 26,
            "question": "Halftime Show: Will Daddy Yankee make a guest appearance?",
            "points": 15,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 27,
            "question": "Halftime Show: Will Bad Bunny change outfits during the performance?",
            "points": 10,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 28,
            "question": "Halftime Show: How long will the halftime show last?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 29,
            "question": "Will the game go into overtime?",
            "points": 10,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 30,
            "question": "What position wins MVP on the winning team?",
            "points": 5,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 31,
            "question": "Will some idiot run on the field during the game?",
            "points": 10,
            "default_answer": 0,
            "type": boolean_type,
        },
        {
            "id": 32,
            "question": "What will the combined score be?",
            "points": 3,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 33,
            "question": "Who will have the most penalties?",
            "points": 15,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 34,
            "question": "What color will the liquid be that they pour on the winning coach?",
            "points": 15,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
        {
            "id": 35,
            "question": "Who wins Puppy Bowl 2026 on Animal Planet?",
            "points": 35,
            "default_answer": 0,
            "type": multiple_choice_type,
        },
    ]

    for q in questions:
        question.objects.update_or_create(
            id=q["id"],
            defaults={
                "question": q["question"],
                "points": q["points"],
                "default_answer": q["default_answer"],
                "type": q["type"],
            },
        )


class Migration(migrations.Migration):
    """
    Seed default Question data
    """

    dependencies = [
        ("core", "0003_seed_question_types"),
    ]

    operations = [
        migrations.RunPython(seed_questions, reverse_code=migrations.RunPython.noop),
    ]
