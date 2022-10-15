from django.conf import settings
from django.core.paginator import Paginator

POSTS_PER_PAGE = settings.POSTS_PER_PAGE


def paginator_(request, posts_list, posts_per_page=POSTS_PER_PAGE):
    paginator = Paginator(posts_list, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
