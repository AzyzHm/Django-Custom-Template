"""End-to-end tests hitting the API exactly as a real client would, over HTTP."""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_unauthenticated_request_is_rejected(api_client):
    response = api_client.get(reverse("item-list"))

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_and_list_item(authenticated_client):
    create_response = authenticated_client.post(
        reverse("item-list"), {"name": "Widget", "description": "From e2e test"}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    assert create_response.data["name"] == "Widget"

    list_response = authenticated_client.get(reverse("item-list"))
    assert list_response.status_code == status.HTTP_200_OK
    assert list_response.data["count"] == 1


@pytest.mark.django_db
def test_retrieve_update_and_delete_item(authenticated_client):
    create_response = authenticated_client.post(reverse("item-list"), {"name": "Widget"})
    item_id = create_response.data["id"]

    retrieve_response = authenticated_client.get(reverse("item-detail", args=[item_id]))
    assert retrieve_response.status_code == status.HTTP_200_OK

    update_response = authenticated_client.put(
        reverse("item-detail", args=[item_id]), {"name": "Renamed"}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.data["name"] == "Renamed"

    delete_response = authenticated_client.delete(reverse("item-detail", args=[item_id]))
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_owner_cannot_access_other_users_item(authenticated_client, other_user):
    from core.repositories.item_repository import ItemRepository

    other_item = ItemRepository.create(owner=other_user, name="Not yours")

    response = authenticated_client.get(reverse("item-detail", args=[other_item.id]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
