from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        response = super(CustomPagination, self).get_paginated_response(data)

        response.data['actual'] = self.page.number
        response.data['total_paginas'] = self.page.paginator.num_pages
        return response
class PaginationDiez(CustomPagination):
    page_size = 10
