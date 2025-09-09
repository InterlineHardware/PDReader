from src.Utilities import *

class Product():

    def __init__(self, sku, model_no, mfg_part_no, brand, title, category: Category, html_desc_feat, status: str, weight=0, weight_unit="", handle="", pack_qty=None, upc ="",tags= "",
                 json_apps="", json_specs="", json_includes="", dimensions: Dimensions=None, resources: Resources=None, media: Media=None, isVariant: bool=False, variantProperties: Variant=None,
                 preSale = False, inventoryPolicy = 'deny', variant_description = "", battery_system=""):
        
        self.handle = handle
        self.sku = sku
        self.modelNo = model_no
        self.mfg_part_no = mfg_part_no
        self.brand = brand
        self.title = title
        self.category = category
        self.upc = upc
        self.tags = tags
        self.HTMLDescription = html_desc_feat
        self.weight = weight
        self.weightUnit = weight_unit
        self.packQuantity = pack_qty
        self.JSONApplications =json_apps
        self.JSONSpecifications = json_specs
        self.JSONIncludes = json_includes
        self.dimensions = dimensions
        self.resources = resources
        self.media = media
        self.isVariant = isVariant
        self.variantProperties = variantProperties
        self.preSale = preSale
        self.inventoryPolicy = inventoryPolicy
        self.variant_description = variant_description
        self.battery_system = battery_system

        if (status == "Active" or status == "Archived" or status == "Draft"):
            self.status = status
        else:
            raise ValueError("status must be either \"Active\" or \"Archived\" or \"Draft\"")
        
        if status == "Active":
            self.isPublished = "TRUE"
        else:
            self.isPublished = "FALSE"
            
        self.publishedScope = "global"
        
    def __str__(self) -> str:
        
        return (f"""SKU: {self.sku}\nModel #: {self.modelNo}\nMfg_part_no: {self.mfg_part_no}\nBrand: {self.brand}\nStatus: {self.status}\nisPublished: {self.isPublished}\nPublished Scope: {self.publishedScope}"""
                f"""Handle: {self.handle}\nTitle: {self.title}\n"""
                f"""HTML Description Features: {self.HTMLDescription}\nJSON Includes: {self.JSONIncludes}\nJSON Applications: {self.JSONApplications}\n"""
                f"""HTML Specifications: {self.JSONSpecifications}\nWeight: {self.weight}\nWeight Unit: {self.weightUnit}\nPack Quantity: {self.packQuantity}\n"""
                f"""Resources:\n{self.resources}\nMedia:\n{self.media}\nBattery System:\n{self.battery_system}""")


#=============================================================================================================================================================#
#=============================================================================================================================================================#

class PDRow():
    # Represent one Row in a PD File
    def __init__(self, interline_sku, manufacturer_model_no,  status: bool, manufacturer_part_no="", upc="", warehouse="", is_online: bool=False, brand="",
                 title="", is_variant: bool=False, option1_name="", option1_value="", option2_name="", option2_value="",
                 option3_name="", option3_value="", option4_name="", option4_value="", pack_quantity="", category1="",
                 category2="", category3="", category4="", tags="", description="", html_desc_features="", json_includes="",
                 json_applications="", json_specs="", images="", videos="", more_info_url="", tds="", sds="", spec_sheet="",
                 alt_res_name="", alt_res_value="", assembled_length="", assembled_width="", assembled_height="",
                 assembled_depth="", assembled_weight="", assembled_operating_weight="", packaged_length="",
                 packaged_width="", packaged_height="", packaged_depth="", packaged_weight="", volume="", html_dimensions="",
                 concatenated_features="", concatenated_includes="", concatenated_specs="", concatenated_applications="", preSale = False, InventoryPolicy = 'deny',
                  variant_description = "", battery_system = "" ):
        
        self.interline_sku = interline_sku
        self.manufacturer_part_no = manufacturer_part_no
        self.manufacturer_model_no = manufacturer_model_no
        self.upc = upc
        self.warehouse = warehouse
        self.status = status
        self.is_online = is_online
        self.brand = brand
        self.title = title
        self.isVariant = is_variant
        if is_variant:
            self.variantProperties = Variant(option1_name, option1_value, option2_name, option2_value, option3_name, option3_value, option4_name, option4_value)
        else:
            self.variantProperties = None
        self.pack_quantity = pack_quantity
        self.category = Category(category1, category2, category3, category4)
        self.tags = tags
        self.description = description
        self.html_desc_features = html_desc_features
        self.json_includes = json_includes
        self.json_applications = json_applications
        self.json_specs = json_specs
        self.images = images
        self.videos = videos
        self.resources = Resources(sds=sds, tds=tds, spec_sheet=spec_sheet, more_info=more_info_url, alternate_res_name=alt_res_name, alternate_res_value=alt_res_value)
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
        self.html_dimensions = html_dimensions
        self.concatenated_features = concatenated_features
        self.concatenated_includes = concatenated_includes
        self.concatenated_specs = concatenated_specs
        self.concatenated_applications = concatenated_applications
        self.preSale =preSale
        self.inventoryPolicy = InventoryPolicy
        self.variant_description = variant_description
        self.battery_system = battery_system

    def __str__(self):
        return (f"PDRow(interline_sku='{self.interline_sku}', manufacturer_part_no='{self.manufacturer_part_no}', manufacturer_model_no='{self.manufacturer_model_no}', upc='{self.upc}', "
                f"warehouse='{self.warehouse}', status='{self.status}', is_online={self.is_online}, brand='{self.brand}', title='{self.title}', "
                f"is_variant={self.isVariant}, option1_name='{self.variantProperties.option1.name if self.isVariant else None}', "
                f"option1_value='{self.variantProperties.option1.value if self.isVariant else None}', "
                f"option2_name='{self.variantProperties.option2.name if self.isVariant else None}', "
                f"option2_value='{self.variantProperties.option2.value if self.isVariant else None}', "
                f"option3_name='{self.variantProperties.option3.name if self.isVariant else None}', "
                f"option3_value='{self.variantProperties.option3.value if self.isVariant else None}', "
                f"option4_name='{self.variantProperties.option4.name if self.isVariant else None}', "
                f"option4_value='{self.variantProperties.option4.value if self.isVariant else None}', "
                f"pack_quantity='{self.pack_quantity}', category1='{self.category.c1}', category2='{self.category.c2}', "
                f"category3='{self.category.c3}', category4='{self.category.c4}', tags='{self.tags}', battery_system='{self.battery_system}', description='{self.description}', "
                f"html_desc_features='{self.html_desc_features}', variant_description = '{self.variant_description}', json_includes='{self.json_includes}', "
                f"json_applications='{self.json_applications}', json_specs='{self.json_specs}', images='{self.images}', "
                f"videos='{self.videos}', more_info_url='{self.resources.moreInfoURL}', tds='{self.resources.tds}', sds='{self.resources.sds}', "
                f"spec_sheet='{self.resources.specSheet}', alt_res_name='{self.resources.alternateResource.name}', alt_res_value='{self.resources.alternateResource.url}', "
                f"assembled_length='{self.assembled_length}', assembled_width='{self.assembled_width}', "
                f"assembled_height='{self.assembled_height}', assembled_depth='{self.assembled_depth}', "
                f"assembled_weight='{self.assembled_weight}', assembled_operating_weight='{self.assembled_operating_weight}', "
                f"packaged_length='{self.packaged_length}', packaged_width='{self.packaged_width}', "
                f"packaged_height='{self.packaged_height}', packaged_depth='{self.packaged_depth}', "
                f"packaged_weight='{self.packaged_weight}', volume='{self.volume}', html_dimensions='{self.html_dimensions}', "
                f"concatenated_features='{self.concatenated_features}', concatenated_includes='{self.concatenated_includes}', "
                f"concatenated_specs='{self.concatenated_specs}', concatenated_applications='{self.concatenated_applications}')")