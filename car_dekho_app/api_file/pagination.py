from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class ReviewListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 2
    last_page_strings = 'last'
    
class ReviewListLimitOffset(LimitOffsetPagination):
    default_limit = 2