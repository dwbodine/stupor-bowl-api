"""
Django models
"""

from django.db import models


class AppSettings(models.Model):
    registration_open = models.BooleanField(default=True)
    results_published = models.BooleanField(default=False)

    def __str__(self):
        return "App Settings"


class Users(models.Model):
    """
    Represents a user in the system
    """

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Users Meta
        """

        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>"


class QuestionType(models.Model):
    """
    Type of question
    """

    id = models.PositiveSmallIntegerField(primary_key=True)
    type = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        QuestionType Meta
        """

        db_table = "question_types"
        verbose_name = "Question Type"
        verbose_name_plural = "Question Types"
        ordering = ["type"]

    def __str__(self) -> str:
        return f"{self.type}"


class Question(models.Model):
    """
    Represents a stupor bowl question
    """

    id = models.PositiveSmallIntegerField(primary_key=True)
    question = models.TextField()
    points = models.IntegerField(null=True, blank=True)
    default_answer = models.IntegerField(default=0)
    actual_answer = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    type = models.ForeignKey(
        QuestionType,
        on_delete=models.DO_NOTHING,
        related_name="questions",
    )

    class Meta:
        """
        Question Meta
        """

        db_table = "questions"
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["id"]

    def __str__(self) -> str:
        text = str(self.question)
        return f"Q{self.id}: {text[:60]}"


class Team(models.Model):
    """
    Static lookup table for teams.
    Intended to be seeded once and not changed.
    """

    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Team Meta
        """

        db_table = "teams"
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class MultipleChoice(models.Model):
    """
    Choices for multiple choice questions
    """

    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING, related_name="choices"
    )
    choice = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()    

    class Meta:
        """
        MultipleChoice Meta
        """
        db_table = "multiple_choices"
        verbose_name = "Multiple Choice"
        verbose_name_plural = "Multiple Choices"
        ordering = ["question", "order"]
        indexes = [
            models.Index(fields=["question", "order"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "order"],
                name="uniq_choice_per_question_order",
            ),
            models.UniqueConstraint(
                fields=["question", "choice"],
                name="uniq_choice_per_question_text",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.order}. {self.choice}"


class Answer(models.Model):
    """
    Records a user answer
    """

    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        Users,
        on_delete=models.DO_NOTHING,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.DO_NOTHING,
        related_name="answers",
    )

    value = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Answer Meta
        """

        db_table = "answers"
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ["question", "user"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="uniq_answer_user_question",
            )
        ]

    def __str__(self) -> str:
        return f"Answer(user={self.user}, question={self.question}, value={self.value})"
