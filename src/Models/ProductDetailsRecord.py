class ProductDetailsRecord:
    def __init__(
        self,
        modelno: str,
        inventory_id=None,
        search_keywords=None,
        product_name=None,
        description=None,
        features=None,
        includes=None,
        specs=None,
        images=None,
        video=None,
        sds=None,
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

        # New fields for assembled and packaged dimensions/weight
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

    def insertRecord(self):
        values = [
            self.modelno,
            self.inventory_id,
            self.search_keywords,
            self.product_name,
            self.description,
            self.features,
            self.includes,
            self.specs,
            self.images,
            self.video,
            self.sds,
            self.assembled_length,
            self.assembled_width,
            self.assembled_height,
            self.assembled_depth,
            self.assembled_weight,
            self.assembled_operating_weight,
            self.packaged_length,
            self.packaged_width,
            self.packaged_height,
            self.packaged_depth,
            self.packaged_weight,
            self.volume,
        ]
        # Replace empty values with None
        return [value if value not in ("", 0, None) else None for value in values]

    def buildUpdateQuery(self):
        fields = {
            "search_keywords": self.search_keywords,
            "product_name": self.product_name,
            "description": self.description,
            "features": self.features,
            "includes": self.includes,
            "specs": self.specs,
            "images": self.images,
            "video": self.video,
            "sds": self.sds,
            "AssembledLength": self.assembled_length,
            "AssembledWidth": self.assembled_width,
            "AssembledHeight": self.assembled_height,
            "AssembledDepth": self.assembled_depth,
            "AssembledWeight": self.assembled_weight,
            "AssembledOperatingWeight": self.assembled_operating_weight,
            "PackagedLength": self.packaged_length,
            "PackagedWidth": self.packaged_width,
            "PackagedHeight": self.packaged_height,
            "PackagedDepth": self.packaged_depth,
            "PackagedWeight": self.packaged_weight,
            "Volume": self.volume,
        }
        # Filter out fields with None values and convert empty strings to None
        non_null_fields = {
            key: value for key, value in fields.items() if value not in ("", 0, None)
        }

        if not non_null_fields:
            return None, []

        # Build the SET clause
        set_clause = ", ".join([f"{key} = %s" for key in non_null_fields])
        parameters = list(non_null_fields.values())

        # Append the inventory_id to the parameters for the WHERE clause
        parameters.append(self.inventory_id)

        # Construct the final SQL query
        update_query = f"""
            UPDATE ProductDetails
            SET {set_clause}
            WHERE inventory_id = %s;
        """
        return update_query, parameters

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
            f"Packaged Weight: {self.packaged_weight}, Volume: {self.volume}"
        )
