# Run local development server
.PHONY: runlocal
runlocal:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.development python manage.py runserver 127.0.0.1:8000

# Run server
.PHONY: run
run:
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.production gunicorn dmitbud.wsgi --workers 5 --bind 0.0.0.0:8000

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
	PGSERVICEFILE=$(CURDIR)/secrets/pg_service.conf DJANGO_SETTINGS_MODULE=dmitbud.settings.production python manage.py migrate

# Upload article as draft
.PHONY: upload
upload:
ifndef ARTICLE
	$(error Usage: make upload ARTICLE=/path/to/article.md)
endif
	python manage.py upload $(ARTICLE)
