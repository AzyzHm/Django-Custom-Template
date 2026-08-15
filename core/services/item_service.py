"""
Business logic layer for Item.

Views call into services; services call the repository layer for
persistence. No ORM access happens outside the repository layer.
"""
from core.exceptions import ItemNotFoundError, PermissionDeniedError
from core.repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository | None = None) -> None:
        self.repository = repository or ItemRepository()

    def list_items(self, owner):
        return self.repository.list_for_owner(owner)

    def get_item(self, item_id: int, owner):
        item = self.repository.get_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        if item.owner_id != owner.id:
            raise PermissionDeniedError()
        return item

    def create_item(self, owner, name: str, description: str = "", is_active: bool = True):
        return self.repository.create(
            owner=owner, name=name, description=description, is_active=is_active
        )

    def update_item(self, item_id: int, owner, **fields):
        item = self.get_item(item_id, owner)
        return self.repository.update(item, **fields)

    def delete_item(self, item_id: int, owner) -> None:
        item = self.get_item(item_id, owner)
        self.repository.delete(item)
