class ItemNotFoundError(Exception):
    """Raised when a requested Item does not exist."""

    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item with id={item_id} was not found.")


class PermissionDeniedError(Exception):
    """Raised when the current user is not permitted to act on a resource."""

    def __init__(self):
        super().__init__("You do not have permission to access this item.")
