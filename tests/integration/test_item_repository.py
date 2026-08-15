"""Integration tests for ItemRepository. Exercises the real ORM against the test database."""

import pytest

from core.repositories.item_repository import ItemRepository


@pytest.mark.django_db
def test_create_and_get_by_id(user):
    item = ItemRepository.create(owner=user, name="Widget", description="A test widget")

    fetched = ItemRepository.get_by_id(item.id)

    assert fetched is not None
    assert fetched.name == "Widget"
    assert fetched.owner_id == user.id


@pytest.mark.django_db
def test_get_by_id_returns_none_when_missing():
    assert ItemRepository.get_by_id(999) is None


@pytest.mark.django_db
def test_list_for_owner_excludes_other_users_items(user, other_user):
    ItemRepository.create(owner=user, name="Mine")
    ItemRepository.create(owner=other_user, name="Not mine")

    items = list(ItemRepository.list_for_owner(user))

    assert len(items) == 1
    assert items[0].name == "Mine"


@pytest.mark.django_db
def test_update_persists_changes(user):
    item = ItemRepository.create(owner=user, name="Original")

    updated = ItemRepository.update(item, name="Renamed")

    assert updated.name == "Renamed"
    item.refresh_from_db()
    assert item.name == "Renamed"


@pytest.mark.django_db
def test_delete_removes_item(user):
    item = ItemRepository.create(owner=user, name="Temporary")
    item_id = item.id

    ItemRepository.delete(item)

    assert ItemRepository.get_by_id(item_id) is None
