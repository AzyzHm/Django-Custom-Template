"""
Data access layer for the Item model.

This is the only layer permitted to run ORM queries directly. Services must
go through the repository rather than touching the ORM themselves, keeping
persistence concerns isolated from business logic.
"""
from django.db.models import QuerySet

from core.models import Item


class ItemRepository:
    @staticmethod
    def list_for_owner(owner) -> QuerySet[Item]:
        return Item.objects.filter(owner=owner)

    @staticmethod
    def get_by_id(item_id: int) -> Item | None:
        return Item.objects.filter(id=item_id).first()

    @staticmethod
    def create(*, owner, name: str, description: str = "", is_active: bool = True) -> Item:
        return Item.objects.create(
            owner=owner, name=name, description=description, is_active=is_active
        )

    @staticmethod
    def update(item: Item, **fields) -> Item:
        for field, value in fields.items():
            setattr(item, field, value)
        item.save(update_fields=[*fields.keys(), "updated_at"])
        return item

    @staticmethod
    def delete(item: Item) -> None:
        item.delete()
