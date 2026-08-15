"""Unit tests for ItemService. The repository is mocked, so no database is touched."""

from unittest.mock import MagicMock

import pytest

from core.exceptions import ItemNotFoundError, PermissionDeniedError
from core.services.item_service import ItemService


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    return ItemService(repository=mock_repository)


def test_get_item_raises_not_found(service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ItemNotFoundError):
        service.get_item(item_id=1, owner=MagicMock(id=1))


def test_get_item_raises_permission_denied_for_other_owner(service, mock_repository):
    fake_item = MagicMock(owner_id=99)
    mock_repository.get_by_id.return_value = fake_item

    with pytest.raises(PermissionDeniedError):
        service.get_item(item_id=1, owner=MagicMock(id=1))


def test_get_item_returns_item_for_matching_owner(service, mock_repository):
    fake_item = MagicMock(owner_id=1)
    mock_repository.get_by_id.return_value = fake_item

    result = service.get_item(item_id=1, owner=MagicMock(id=1))

    assert result is fake_item


def test_create_item_delegates_to_repository(service, mock_repository):
    owner = MagicMock(id=1)

    service.create_item(owner=owner, name="Widget")

    mock_repository.create.assert_called_once_with(
        owner=owner, name="Widget", description="", is_active=True
    )


def test_delete_item_checks_ownership_before_deleting(service, mock_repository):
    fake_item = MagicMock(owner_id=99)
    mock_repository.get_by_id.return_value = fake_item

    with pytest.raises(PermissionDeniedError):
        service.delete_item(item_id=1, owner=MagicMock(id=1))

    mock_repository.delete.assert_not_called()
