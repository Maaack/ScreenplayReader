from rest_framework.decorators import detail_route
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .pagination import StandardResultsSetPagination


class BaseListView(ListCreateAPIView):
    """
    List all object instances, or create a new object instance.
    """
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    class Meta:
        abstract = True


class BaseDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an object instance.
    """
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    class Meta:
        abstract = True


class BaseViewSet(ModelViewSet):
    """
    Retrieve, update or delete an object instance.
    """
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    class Meta:
        abstract = True


class OperationViewSet(BaseViewSet):
    class Meta:
        abstract = True

    @detail_route(methods=['post'],  url_path='run-operation')
    def run_operation(self, request, pk = None):
        operation = self.get_object()
        operation.run_operation()
        return Response('Operation complete!')