from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render

from .controller import (
    get_article_by_slug,
    get_last_articles,
    get_streams,
)
from .models import Article


def is_user_superuser(request):
    return request.user.is_authenticated and request.user.is_superuser


def render_feed(request, article_list):
    context = {
        "article_list": article_list,
        "stream_list": get_streams(),
    }
    return render(request, "blog/index.html", context)


def feed(request):
    get_published_only = not is_user_superuser(request)
    article_list = get_last_articles(get_published_only)
    return render_feed(request, article_list)


def linux(request):
    get_published_only = not is_user_superuser(request)
    article_list = get_last_articles(
        get_published_only, stream="linux",
    )
    return render_feed(request, article_list)


def html(request):
    get_published_only = not is_user_superuser(request)
    article_list =  get_last_articles(
        get_published_only, stream="html",
    )
    return render_feed(request, article_list)


def page(request, page):
    return HttpResponse(f"You're on the page {page}")


def read(request, slug):
    try:
        article = get_article_by_slug(slug)
    except Article.DoesNotExist as error:
        raise Http404("Article not found") from error

    if not is_user_superuser(request):
        if not article.is_published():
            raise PermissionDenied

    context = {
        "article": article,
        "stream_list": get_streams(),
    }

    return render(request, "blog/article.html", context)
