from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Paginate(PageNumberPagination):

    """
        custom pagination using PageNumberPagination from rest_framework
        @retrun Response :{
            'query': the word is using in query param,
            'number_of_pages': the number of pages ,
            'page_number': the nubmer of current page,
            'next_page_number': number for next page if has or none,
            'previous_page_number': number fro previous page if has or none ,
            'data': object has serializers data 
        }
    """

    page_size = 10

    def get_paginated_response(self, data):

        if self.page.has_previous():
            previous = self.page.previous_page_number()
        else:
            previous = None
        if self.page.has_next():
            next = self.page.next_page_number()
        else:
            next = None

        # print(next)
        return Response(data={
            'query': self.page_query_param,
            'number_of_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'next_page_number': next,
            'previous_page_number': previous,
            'data': data
        })
