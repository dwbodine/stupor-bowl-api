#!/bin/sh
set -eu

python manage.py migrate --noinput

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ]; then
  python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
email = os.environ["DJANGO_SUPERUSER_EMAIL"]

u, created = User.objects.get_or_create(username=username, defaults={"email": email})
u.email = email
u.is_staff = True
u.is_superuser = True
u.set_password(password)
u.save()

print(("Created" if created else "Updated") + f" superuser: {username}")
PY
fi
