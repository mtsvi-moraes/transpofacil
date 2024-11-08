from ..models.item_model import Item

def get_item(item_id: int) -> Item:
    return Item(id=item_id, name="Sample Item", description="This is a sample item")
