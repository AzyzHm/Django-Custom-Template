from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.exceptions import ItemNotFoundError, PermissionDeniedError
from core.serializers.item import ItemSerializer
from core.services.item_service import ItemService


class ItemViewSet(viewsets.ViewSet):
    """CRUD endpoints for Item, delegating all logic to the service layer."""

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ItemService()

    def list(self, request):
        items = self.service.list_items(owner=request.user)
        page = self.paginate_queryset(items, request)
        serializer = ItemSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = self.service.create_item(owner=request.user, **serializer.validated_data)
        return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            item = self.service.get_item(int(pk), owner=request.user)
        except ItemNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDeniedError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(ItemSerializer(item).data)

    def update(self, request, pk=None):
        serializer = ItemSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            item = self.service.update_item(
                int(pk), owner=request.user, **serializer.validated_data
            )
        except ItemNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDeniedError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(ItemSerializer(item).data)

    def destroy(self, request, pk=None):
        try:
            self.service.delete_item(int(pk), owner=request.user)
        except ItemNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDeniedError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def paginate_queryset(self, queryset, request):
        if not hasattr(self, "paginator"):
            from rest_framework.pagination import PageNumberPagination

            self.paginator = PageNumberPagination()
        return self.paginator.paginate_queryset(queryset, request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)
