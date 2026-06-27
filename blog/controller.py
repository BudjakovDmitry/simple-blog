from django.db.models.functions import Coalesce

from .models import Article, Stream


DEFAULT_ARTICLES_LIMIT = 10


def order_by_publication_date(queryset):
    return queryset.alias(sort_date=Coalesce("published_at", "created_at")).order_by("-sort_date")


def get_last_articles(
    published_only: bool = True,
    count: int = DEFAULT_ARTICLES_LIMIT,
    stream: str | None = None,
):
    articles = Article.objects.all()
    if published_only:
        articles = articles.filter(status=Article.Status.PUBLISHED)
    if stream:
        articles = articles.filter(stream__route=stream)

    return order_by_publication_date(articles)[:count]


def get_article_by_slug(slug: str) -> Article:
    return Article.objects.get(slug=slug)


def get_streams():
    return Stream.objects.order_by("order")
