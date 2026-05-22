"""
Django admin registrations for core models.
"""

from django.contrib import admin

from .models import (
    Answer,
    AppSettings,
    MultipleChoice,
    Question,
    QuestionType,
    Team,
    Users,
)


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "registration_open", "results_published")
    list_editable = (
        "registration_open",
        "results_published",
    )  # optional: toggle right from the list


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    """
    Docstring for UsersAdmin
    """

    list_display = (
        "id",
        "last_name",
        "first_name",
        "email",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = ("first_name", "last_name", "email")
    ordering = ("last_name", "first_name")
    readonly_fields = ("created_at", "updated_at")


class MultipleChoiceInline(admin.TabularInline):
    """
    Docstring for MultipleChoiceInline
    """

    model = MultipleChoice
    extra = 0
    fields = ("order", "choice")
    ordering = ("order",)
    show_change_link = True


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    """
    Docstring for QuestionTypeAdmin
    """

    list_display = ("id", "type")
    search_fields = ("type",)
    ordering = ("type",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Docstring for QuestionAdmin
    """

    list_display = (
        "id",
        "type",
        "question_short",
        "points",
        "default_answer",
        "actual_answer",
    )
    list_filter = ("type",)
    search_fields = ("id", "question", "notes")
    ordering = ("id",)
    readonly_fields = ()
    inlines = (MultipleChoiceInline,)

    fieldsets = (
        (None, {"fields": ("id", "type", "question")}),
        ("Scoring", {"fields": ("points", "default_answer", "actual_answer")}),
        ("Notes", {"fields": ("notes",)}),
    )

    @admin.display(description="Question")
    def question_short(self, obj: Question) -> str:
        """
        Docstring for question_short

        :param self: Description
        :param obj: Description
        :type obj: Question
        :return: Description
        :rtype: str
        """
        return str(obj.question)[:80]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Docstring for TeamAdmin
    """

    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)

    # Optional: keep teams "static" in admin
    def has_add_permission(self, request):
        return True  # set to False if you never want adding in admin

    def has_delete_permission(self, request, obj=None):
        return True  # set to False if you never want deleting in admin


@admin.register(MultipleChoice)
class MultipleChoiceAdmin(admin.ModelAdmin):
    """
    Docstring for MultipleChoiceAdmin
    """

    list_display = ("id", "question", "order", "choice")
    list_filter = ("question",)
    search_fields = ("choice", "question__question")
    ordering = ("question__id", "order")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Docstring for AnswerAdmin
    """

    list_display = ("id", "user", "question", "value", "created_at", "updated_at")
    list_filter = ("question", "created_at")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "question__question",
    )
    ordering = ("question__id", "user__last_name", "user__first_name")
    readonly_fields = ("created_at", "updated_at")
