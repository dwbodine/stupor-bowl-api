from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def graphql_view(request, *args, **kwargs):
    """
    Lazy GraphQL view so Django management commands (migrate, makemigrations, etc.)
    don't build the Strawberry schema at import time.
    """
    from strawberry.django.views import GraphQLView
    from core.graphql import schema

    view = GraphQLView.as_view(schema=schema, graphiql=settings.DEBUG)
    return view(request, *args, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", graphql_view),
]
