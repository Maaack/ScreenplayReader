from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def default_process_list_request(request, serializer_class, object_class):
    if request.method == 'GET':
        objects = object_class.objects.all()
        serializer = serializer_class(objects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def default_process_detail_request(request, serializer_class, object_instance):
    if request.method == 'GET':
        serializer = serializer_class(object_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializer_class(object_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        object_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseListView(ListCreateAPIView):
    """
    List all object instances, or create a new object instance.
    """
    permission_classes = (AllowAny,)

    class Meta:
        abstract = True


class BaseDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an object instance.
    """
    permission_classes = (AllowAny,)

    class Meta:
        abstract = True


class BaseViewSet(ModelViewSet):
    """
    Retrieve, update or delete an object instance.
    """
    permission_classes = (AllowAny,)

    class Meta:
        abstract = True
