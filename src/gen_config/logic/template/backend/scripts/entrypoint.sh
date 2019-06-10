#!/bin/sh
set -e

# Setup database automatically if needed
DB_CHECK_STATUS=$(python {{TAIGA_HOME}}/scripts/checkdb.py)
if [[ "$DB_CHECK_STATUS" == "missing_django_migrations" ]]; then
  echo "Configuring initial database"
  python {{TAIGA_HOME}}/taiga-back/manage.py migrate --noinput
  python {{TAIGA_HOME}}/taiga-back/manage.py loaddata initial_user
  python {{TAIGA_HOME}}/taiga-back/manage.py loaddata initial_project_templates
  python {{TAIGA_HOME}}/taiga-back/manage.py compilemessages
  python {{TAIGA_HOME}}/taiga-back/manage.py collectstatic --noinput
fi

# Look for static folder, if it does not exist, then generate it
if [ "$(ls -A /taiga_backend/static-root/ 2> /dev/null)" == "" ]; then
  python {{TAIGA_HOME}}/taiga-back/manage.py collectstatic --noinput
fi

exec "$@"
