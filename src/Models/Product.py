class PDRow:
    def __init__(
        self,
        modelno,
        inventory_id,
        search_keywords,
        product_name,
        description,
        features,
        includes,
        specs,
        images,
        video,
        sds,
        assembled_length=None,
        assembled_width=None,
        assembled_height=None,
        assembled_depth=None,
        assembled_weight=None,
        assembled_operating_weight=None,
        packaged_length=None,
        packaged_width=None,
        packaged_height=None,
        packaged_depth=None,
        packaged_weight=None,
        volume=None,
        sell_price=None,         # New field for selling price
        show_online_date=None,   # New field for online date
    ):
        self.modelno = modelno
        self.inventory_id = inventory_id
        self.search_keywords = search_keywords
        self.product_name = product_name
        self.description = description
        self.features = features
        self.includes = includes
        self.specs = specs
        self.images = images
        self.video = video
        self.sds = sds
        self.assembled_length = assembled_length
        self.assembled_width = assembled_width
        self.assembled_height = assembled_height
        self.assembled_depth = assembled_depth
        self.assembled_weight = assembled_weight
        self.assembled_operating_weight = assembled_operating_weight
        self.packaged_length = packaged_length
        self.packaged_width = packaged_width
        self.packaged_height = packaged_height
        self.packaged_depth = packaged_depth
        self.packaged_weight = packaged_weight
        self.volume = volume
        self.sell_price = sell_price           # Set the sell price
        self.show_online_date = show_online_date # Set the online date

    def __str__(self) -> str:
        return (
            f"Model Number: {self.modelno}, Inventory ID: {self.inventory_id}, "
            f"Search Keywords: {self.search_keywords}, Product Name: {self.product_name}, "
            f"Description: {self.description}, Features: {self.features}, "
            f"Includes: {self.includes}, Specs: {self.specs}, Images: {self.images}, "
            f"Video: {self.video}, SDS: {self.sds}, Assembled Length: {self.assembled_length}, "
            f"Assembled Width: {self.assembled_width}, Assembled Height: {self.assembled_height}, "
            f"Assembled Depth: {self.assembled_depth}, Assembled Weight: {self.assembled_weight}, "
            f"Assembled Operating Weight: {self.assembled_operating_weight}, "
            f"Packaged Length: {self.packaged_length}, Packaged Width: {self.packaged_width}, "
            f"Packaged Height: {self.packaged_height}, Packaged Depth: {self.packaged_depth}, "
            f"Packaged Weight: {self.packaged_weight}, Volume: {self.volume}, "
            f"Sell Price: {self.sell_price}, Show Online Date: {self.show_online_date}"  # Include new fields in string representation
        )