from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.core.models import Page
from wagtail.search.models import Query

from brahms.home.models import HomePage


def search(request):
    search_query = request.GET.get('query', None)
    if search_query:
        if 'elasticsearch' in settings.WAGTAILSEARCH_BACKENDS['default']['BACKEND']:
            # In production, use ElasticSearch and a simplified search query, per
            # https://docs.wagtail.io/en/latest/topics/search/backends.html
            # like this:
            search_results = Page.objects.live().search(search_query)
        else:
            # If we aren't using ElasticSearch for the demo, fall back to native db search.
            # But native DB search can't search specific fields in our models on a `Page` query.
            # So for demo purposes ONLY, we hard-code in the model names we want to search.
            home_results = HomePage.objects.live().search(search_query)
            home_page_ids = [p.page_ptr.id for p in home_results]
            search_results = Page.objects.live().filter(id__in=home_page_ids)

        query = Query.get(search_query)

        # Record hit
        query.add_hit()

    else:
        search_results = Page.objects.none()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
