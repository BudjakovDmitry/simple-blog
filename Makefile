# Run local development server
.PHONY: runlocal
runlocal:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.development python manage.py runserver 127.0.0.1:8000

# Run server
.PHONY: run
run:
	PGSERVICEFILE=/etc/dmitbud/postgres/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.production gunicorn dmitbud.wsgi --workers 5 --bind 127.0.0.1:8000

# Make migrations
.PHONY: migrations
migrations:
	python manage.py makemigrations

# Apply migrations locally
.PHONY: migratelocal
migratelocal:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.development python manage.py migrate

# Apply migrations in production
.PHONY: migrate
migrate:
	PGSERVICEFILE=/etc/dmitbud/postgres/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.production python manage.py migrate

# Collect static files for production
.PHONY: collectstatic
collectstatic:
	DJANGO_SETTINGS_MODULE=dmitbud.settings.production python manage.py collectstatic --noinput

# Create superuser in production
.PHONY: superuser
superuser:
	PGSERVICEFILE=/etc/dmitbud/postgres/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.production python manage.py createsuperuser

# Create local superuser
.PHONY: superuserlocal
superuserlocal:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.development python manage.py createsuperuser

# Run shell local
.PHONY: shelllocal
shellloccal:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.development python manage.py shell


# Upload article as draft locally
.PHONY: uploadlocal
uploadlocal:
ifndef ARTICLE
	$(error Usage: make upload ARTICLE=/path/to/article.md)
endif
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.development python manage.py upload $(ARTICLE)

# Upload article as draft
.PHONY: upload
upload:
ifndef ARTICLE
	$(error Usage: make upload ARTICLE=/path/to/article.md)
endif
	PGSERVICEFILE=/etc/dmitbud/postgres/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.production make upload $(ARTICLE)
