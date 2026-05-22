# core/graphql.py
from __future__ import annotations

from typing import List, Optional, cast

from django.db import IntegrityError, transaction
import strawberry
import strawberry_django
from strawberry.permission import BasePermission
from strawberry.types import Info

from django.db.models import Case, When, Value, IntegerField, Sum, Count, F, Q
from django.db.models.functions import Coalesce

from .models import (
    Answer,
    AppSettings,
    MultipleChoice,
    Question,
    QuestionType,
    Team,
    Users,
)


# -----------------------
# Permissions
# -----------------------
class IsStaff(BasePermission):
    message = "You must be a staff user to perform this action."

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        request = info.context.request
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


# -----------------------
# Strawberry Types (Django-backed)
# -----------------------
@strawberry_django.type(Users)
class UsersType:
    id: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    email: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry_django.type(QuestionType)
class QuestionTypeType:
    id: strawberry.auto
    type: strawberry.auto


@strawberry_django.type(Question)
class QuestionTypeGQL:
    id: strawberry.auto
    question: strawberry.auto
    points: strawberry.auto
    default_answer: strawberry.auto
    actual_answer: strawberry.auto
    notes: strawberry.auto
    type: QuestionTypeType


@strawberry_django.type(Team)
class TeamType:
    id: strawberry.auto
    name: strawberry.auto


@strawberry_django.type(MultipleChoice)
class MultipleChoiceType:
    id: strawberry.auto
    # You can expose the question object, but most clients only need question_id
    question: QuestionTypeGQL
    choice: strawberry.auto
    order: strawberry.auto


@strawberry_django.type(Answer)
class AnswerType:
    id: strawberry.auto
    user: UsersType
    question: QuestionTypeGQL
    value: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.type
class UserGQL:
    id: int
    first_name: str
    last_name: str
    email: str


@strawberry.type
class BooleanOptionType:
    value: int
    label: str


@strawberry.type
class CorrectAnswerGQL:
    question_id: int
    points: int


@strawberry.type
class LeaderboardRowGQL:
    user: UserGQL
    score: int
    correct_count: int
    answered_count: int


@strawberry.type
class QuestionWithOptionsType:
    """
    One question plus possible options depending on its QuestionType.
    NOTE: `question` is a Strawberry type, not a Django model.
    """

    question: QuestionTypeGQL

    @strawberry.field
    def multiple_choices(self) -> list[MultipleChoiceType]:
        qtype = (self.question.type.type or "").lower()
        if qtype not in {"multiplechoice", "multiple choice", "mc"}:
            return []

        qs = (
            MultipleChoice.objects.select_related("question")
            .filter(question_id=self.question.id)
            .order_by("order")
        )
        return cast(list[MultipleChoiceType], list(qs))

    @strawberry.field
    def teams(self) -> list[TeamType]:
        qtype = (self.question.type.type or "").lower()
        if qtype not in {"team", "teams"}:
            return []

        qs = Team.objects.order_by("name")
        return cast(list[TeamType], list(qs))

    @strawberry.field
    def boolean_options(self) -> list[BooleanOptionType]:
        qtype = (self.question.type.type or "").lower()
        if qtype not in {"boolean", "bool", "truefalse", "true/false"}:
            return []
        return [
            BooleanOptionType(value=0, label="No"),
            BooleanOptionType(value=1, label="Yes"),
        ]


# ----------------------
# Helper Functions
# ----------------------
def get_settings():
    return AppSettings.objects.filter(id=1).first()


def registration_is_open() -> bool:
    s = get_settings()
    return True if s is None else bool(s.registration_open)


def results_are_published() -> bool:
    s = get_settings()
    return False if s is None else bool(s.results_published)


def _user_from_row(row) -> UserGQL:
    return UserGQL(
        id=row["user_id"],
        first_name=row["user__first_name"],
        last_name=row["user__last_name"],
        email=row["user__email"],
    )


# -----------------------
# Inputs
# -----------------------
@strawberry.input
class UserInput:
    first_name: str
    last_name: str
    email: str


@strawberry.input
class QuestionInput:
    question: str
    type_id: int
    points: Optional[int] = None
    default_answer: int = 0
    actual_answer: Optional[int] = None
    notes: Optional[str] = None


@strawberry.input
class MultipleChoiceInput:
    question_id: int
    choice: str
    order: int


@strawberry.input
class AnswerInput:
    user_id: int
    question_id: int
    value: Optional[int] = None


@strawberry.input
class AnswerItemInput:
    question_id: int
    value: Optional[int] = None


# -----------------------
# Query
# -----------------------
@strawberry.type
class Query:
    # Lists (Django-optimized)
    users: list[UsersType] = strawberry_django.field()
    question_types: list[QuestionTypeType] = strawberry_django.field()
    questions: list[QuestionTypeGQL] = strawberry_django.field()
    teams: list[TeamType] = strawberry_django.field()
    multiple_choices: list[MultipleChoiceType] = strawberry_django.field()
    answers: list[AnswerType] = strawberry_django.field()

    @strawberry.field
    def registration_open(self) -> bool:
        return registration_is_open()

    @strawberry.field
    def results_published(self) -> bool:
        return results_are_published()

    # Single item helpers
    @strawberry.field
    def user(self, _info: Info, user_id: int) -> Optional[UsersType]:
        return cast(Optional[UsersType], Users.objects.filter(pk=user_id).first())

    @strawberry.field
    def question(self, _info: Info, question_id: int) -> Optional[QuestionTypeGQL]:
        return cast(
            Optional[QuestionTypeGQL],
            Question.objects.select_related("type").filter(pk=question_id).first(),
        )

    # ✅ What you asked for: questions with options
    @strawberry.field
    def questions_with_options(self, _info: Info) -> list[QuestionWithOptionsType]:
        qs = Question.objects.select_related("type").order_by("id")
        # NOTE: passing Django model instances is fine;
        # strawberry-django can marshal them into QuestionTypeGQL
        return [QuestionWithOptionsType(question=q) for q in qs]  # type: ignore[arg-type]

    @strawberry.field
    def answers_for_user(self, _info: Info, user_id: int) -> list[AnswerType]:
        qs = (
            Answer.objects.select_related("user", "question", "question__type")
            .filter(user_id=user_id)
            .order_by("question_id")
        )
        # Strawberry-Django can marshal model instances into AnswerType,
        # but Pylance needs a hint:
        return cast(list[AnswerType], list(qs))
    
    @strawberry.field
    def answers_for_identity(
        self,
        _info: Info,
        first_name: str,
        last_name: str,
        email: str,
    ) -> list[AnswerType]:
        """
        Fetch a user's current answers given first name, last name, AND email.
        Returns [] if identity does not match or user not found.
        """
        first = first_name.strip()
        last = last_name.strip()
        eml = email.strip().lower()

        if not first or not last or not eml:
            return []

        # Email is unique → fetch user deterministically
        user = (
            Users.objects.filter(email=eml)
            .only("id", "first_name", "last_name")
            .first()
        )
        if not user:
            return []

        # Enforce identity match (case-insensitive for names)
        if user.first_name.lower() != first.lower() or user.last_name.lower() != last.lower():
            return []

        qs = (
            Answer.objects.select_related("user", "question", "question__type")
            .filter(user_id=user.id)
            .order_by("question_id")
        )
        return cast(list[AnswerType], list(qs))


    @strawberry.field
    def choices_for_question(
        self, _info: Info, question_id: int
    ) -> list[MultipleChoiceType]:
        mcs = (
            MultipleChoice.objects.select_related("question")
            .filter(question_id=question_id)
            .order_by("order")
        )
        return cast(list[MultipleChoiceType], list(mcs))

    @strawberry.field
    def leaderboard(self) -> List[LeaderboardRowGQL]:
        """
        Score rules:
        - A correct answer is Answer.value == Question.actual_answer
        - score = sum(Question.points) for correct answers
        - correct_count = number of correct answers
        - answered_count = number of answers where value IS NOT NULL
        """

        if not results_are_published():
            raise Exception(
                "Results are not published yet."
            )  # pylint: disable=broad-exception-raised

        qs = (
            Answer.objects.select_related("user")
            .annotate(
                is_correct=Case(
                    When(
                        value=F("question__actual_answer"),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                earned_points=Case(
                    When(
                        value=F("question__actual_answer"),
                        then=Coalesce(F("question__points"), Value(0)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            )
            .values(
                "user_id",
                "user__first_name",
                "user__last_name",
                "user__email",
            )
            .annotate(
                answered_count=Count("id", filter=Q(value__isnull=False)),
                correct_count=Coalesce(Sum("is_correct"), Value(0)),
                score=Coalesce(Sum("earned_points"), Value(0)),
            )
            .order_by("-score", "-correct_count", "user__last_name", "user__first_name")
        )

        return [
            LeaderboardRowGQL(
                user=_user_from_row(row),
                score=int(row["score"] or 0),
                correct_count=int(row["correct_count"] or 0),
                answered_count=int(row["answered_count"] or 0),
            )
            for row in qs
        ]


# -----------------------
# Mutations
# -----------------------
@strawberry.type
class Mutation:
    # -------------------
    # ✅ Public: User self-register
    # -------------------
    @strawberry.mutation
    def register_user(self, _info: Info, data: UserInput) -> UsersType:
        """
        Public: allows a person to create themselves in Users table.
        """
        if not registration_is_open():
            raise Exception(
                "Registration is closed."
            )  # pylint: disable=broad-exception-raised

        first = data.first_name.strip()
        last = data.last_name.strip()
        email = data.email.strip().lower()

        try:
            return cast(
                UsersType,
                Users.objects.create(first_name=first, last_name=last, email=email),
            )
        except IntegrityError as exc:
            raise ValueError("A user with that email already exists.") from exc

    # -------------------
    # ✅ Public: Submit answer (upsert)
    # -------------------
    @strawberry.mutation
    def submit_answer(self, _info: Info, data: AnswerInput) -> AnswerType:
        """
        Public: create or update an answer for (user_id, question_id).
        """
        # Helpful validation (clean errors)
        if not Users.objects.filter(pk=data.user_id).exists():
            raise ValueError("User not found.")
        if not Question.objects.filter(pk=data.question_id).exists():
            raise ValueError("Question not found.")

        obj, _created = Answer.objects.update_or_create(
            user_id=data.user_id,
            question_id=data.question_id,
            defaults={"value": data.value},
        )
        return cast(AnswerType, obj)

    # -------------------
    # Staff-only CRUD (admin tools)
    # -------------------
    @strawberry.mutation(permission_classes=[IsStaff])
    def create_user(self, _info: Info, data: UserInput) -> UsersType:
        return cast(
            UsersType,
            Users.objects.create(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
            ),
        )

    @strawberry.mutation(permission_classes=[IsStaff])
    def update_user(self, _info: Info, user_id: int, data: UserInput) -> UsersType:
        u = Users.objects.get(pk=user_id)
        u.first_name = data.first_name
        u.last_name = data.last_name
        u.email = data.email
        u.save()
        return cast(UsersType, u)

    @strawberry.mutation(permission_classes=[IsStaff])
    def delete_user(self, _info: Info, user_id: int) -> bool:
        Users.objects.filter(pk=user_id).delete()
        return True

    @strawberry.mutation(permission_classes=[IsStaff])
    def create_question(
        self, _info: Info, question_id: int, data: QuestionInput
    ) -> QuestionTypeGQL:
        qt = QuestionType.objects.get(pk=data.type_id)
        q = Question.objects.create(
            id=question_id,  # manual PK
            question=data.question,
            points=data.points,
            default_answer=data.default_answer,
            actual_answer=data.actual_answer,
            notes=data.notes,
            type=qt,
        )
        return cast(QuestionTypeGQL, q)

    @strawberry.mutation(permission_classes=[IsStaff])
    def update_question(
        self, _info: Info, question_id: int, data: QuestionInput
    ) -> QuestionTypeGQL:
        q = Question.objects.get(pk=question_id)
        q.question = data.question
        q.points = data.points
        q.default_answer = data.default_answer
        q.actual_answer = data.actual_answer
        q.notes = data.notes
        q.type = QuestionType.objects.get(pk=data.type_id)
        q.save()
        return cast(QuestionTypeGQL, q)

    @strawberry.mutation(permission_classes=[IsStaff])
    def delete_question(self, _info: Info, question_id: int) -> bool:
        Question.objects.filter(pk=question_id).delete()
        return True

    @strawberry.mutation(permission_classes=[IsStaff])
    def create_multiple_choice(
        self, _info: Info, multiple_choice_id: int, data: MultipleChoiceInput
    ) -> MultipleChoiceType:
        q = Question.objects.get(pk=data.question_id)
        return cast(
            MultipleChoiceType,
            MultipleChoice.objects.create(
                id=multiple_choice_id,  # manual PK
                question=q,
                choice=data.choice,
                order=data.order,
            ),
        )

    @strawberry.mutation(permission_classes=[IsStaff])
    def update_multiple_choice(
        self,
        _info: Info,
        choice_id: int,
        choice: Optional[str] = None,
        order: Optional[int] = None,
    ) -> MultipleChoiceType:
        mc = MultipleChoice.objects.get(pk=choice_id)
        if choice is not None:
            mc.choice = choice
        if order is not None:
            mc.order = order
        mc.save()
        return cast(MultipleChoiceType, mc)

    @strawberry.mutation(permission_classes=[IsStaff])
    def delete_multiple_choice(self, _info: Info, choice_id: int) -> bool:
        MultipleChoice.objects.filter(pk=choice_id).delete()
        return True

    @strawberry.mutation(permission_classes=[IsStaff])
    def upsert_answer(self, _info: Info, data: AnswerInput) -> AnswerType:
        obj, _created = Answer.objects.update_or_create(
            user_id=data.user_id,
            question_id=data.question_id,
            defaults={"value": data.value},
        )
        return cast(AnswerType, obj)

    @strawberry.mutation(permission_classes=[IsStaff])
    def delete_answer(self, _info: Info, user_id: int, question_id: int) -> bool:
        Answer.objects.filter(user_id=user_id, question_id=question_id).delete()
        return True

    @strawberry.mutation
    def submit_answers(
        self,
        _info: Info,
        user_id: int,
        answers: list[AnswerItemInput],
    ) -> list[AnswerType]:
        """
        Public: bulk create/update answers for a user.
        Upserts each (user_id, question_id) using Answer's UniqueConstraint.
        """
        # Ensure user exists (gives a clean error early)
        Users.objects.get(pk=user_id)

        # Optional: validate questions exist (fast single query)
        qids = [a.question_id for a in answers]
        existing_qids = set(
            Question.objects.filter(id__in=qids).values_list("id", flat=True)
        )
        missing = [qid for qid in qids if qid not in existing_qids]
        if missing:
            raise ValueError(f"Invalid question_id(s): {missing}")

        results: list[Answer] = []

        with transaction.atomic():
            for item in answers:
                obj, _created = Answer.objects.update_or_create(
                    user_id=user_id,
                    question_id=item.question_id,
                    defaults={"value": item.value},
                )
                results.append(obj)

        # Return Django models; strawberry-django will marshal to AnswerType
        return cast(list[AnswerType], results)


schema = strawberry.Schema(query=Query, mutation=Mutation)
