from rest_framework.pagination import PageNumberPagination


class SubsPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6
