from rest_framework.pagination import PageNumberPagination


class PaginationFoodgram(PageNumberPagination):
    """
    https://www.django-rest-framework.org/api-guide/pagination/
    """
    page_size_query_param = 'limit'
    page_size = 6
