from src.Products import Product
from src.Utilities import *

class MatrixifyRow:
    
    #Keep like this
    def __init__(self, title="",
                 handle="",
                 bodyHTML="",
                 vendor="",
                 tags="",
                 status="",
                 published="",
                 publishedScope="",
                 images: list="",
                 imagePosition=None,
                 variantID="",
                 option1_name="",
                 option1_value="",
                 option2_name="",
                 option2_value="",
                 option3_name="",
                 option3_value="",
                 variantPosition=None,
                 variantSKU="",
                 variantBarcode ="",
                 variantWeight="",
                 variantWeightUnit="",
                 variantImage="",
                 inventoryPolicy="deny",
                 v_meta_description="",
                 v_meta_includes="",
                 v_meta_applications="",
                 v_meta_specs="",
                 v_meta_packQty="",
                 v_meta_videos: list="",
                 v_meta_sds="",
                 v_meta_tds="",
                 v_meta_specSheet="",
                 v_meta_moreInfoURL="",
                 v_meta_altResName="",
                 v_meta_altResURL="",
                 v_meta_modelNo="",
                 meta_description="",
                 v_meta_MPN  = "",
                 template = "",
                 battery_system = "",
                 assembled_length = "",
                 assembled_width = "",
                 assembled_height = "",
                 assembled_depth = "",
                 assembed_weight = "",
                 packaged_length = "",
                 packaged_width = "",
                 packaged_height = "",
                 volume = ""
                 ):
        
        imageSrc = images[0] if images and len(images) == 1 else ";".join(images) if images else ""
        v_meta_video = v_meta_videos[0] if v_meta_videos and len(v_meta_videos) >= 1 else "" 
        self.row = [handle, "MERGE", title, bodyHTML, vendor, tags, status, template, published, publishedScope, "FALSE", imageSrc, "MERGE", imagePosition, variantID, "MERGE",
                    option1_name, option1_value, option2_name, option2_value, option3_name, option3_value, variantPosition, variantSKU, variantBarcode, variantWeight, 
                    variantWeightUnit,variantImage, "shopify", inventoryPolicy, "manual", v_meta_description, v_meta_includes, v_meta_applications, battery_system, v_meta_specs,
                    v_meta_packQty, v_meta_video, v_meta_sds, v_meta_tds, v_meta_specSheet, v_meta_moreInfoURL, v_meta_altResName, v_meta_altResURL, v_meta_modelNo, 
                    meta_description, v_meta_MPN, assembled_length, assembled_width, assembled_height, assembled_depth, assembed_weight, packaged_length, packaged_width,
                    packaged_height, volume
                    ]

class Matrixify:
    
    #In this class, store any constant values needed, like columns headers for example
    rows = []
    #we want a function in this class that takes in an instance of the Product Class
    #and converts it into rows for the excel sheet. Use the MatrixifyRow class to represent rows
    # def getRows(product : Product) -> list:
    #     productRows = MatrixifyRow(product).to_list()
    #     return productRows

    # It is important to note that for a given input (product), the final output in excel might need several rows (think for variants)
    # So for a given product, the function must return a list of lists back to the excel processor. The outer list represents the product,
    # while the inner lists represent the rows for that product
    
    columns = ["Handle", "Command", "Title", "Body HTML", "Vendor", "Tags", "Status", "Template Suffix", "Published", "Published Scope", "Gift Card", "Image Src", 
               "Image Command", "Image Position", "Variant ID", "Variant Command", 
               "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value", "Variant Position",
               "Variant SKU", "Variant Barcode", "Variant Weight", "Variant Weight Unit", "Variant Image", "Variant Inventory Tracker", "Variant Inventory Policy", 
               "Variant Fulfillment Service", "Variant Metafield: custom.variant_description", "Variant Metafield: custom.variant_includes", 
               "Variant Metafield: custom.variant_applications", "Metafield: custom.battery_system" ,"Variant Metafield: custom.variant_specifications",
               "Variant Metafield: custom.pack_qty", "Variant Metafield: custom.video_url", "Variant Metafield: custom.sds", 
               "Variant Metafield: custom.tds", "Variant Metafield: custom.spec_sheet_url", 
               "Variant Metafield: custom.more_info_url", "Variant Metafield: custom.alternate_resource_1_name", "Variant Metafield: custom.alternate_resource_1_url", 
               "Variant Metafield: custom.manufacturer_model_number", "Metafield: description_tag", "Variant Metafield: mm-google-shopping.mpn",
               "Variant Metafield: dimensions.assembled_length", "Variant Metafield: dimensions.assembled_width", "Variant Metafield: dimensions.assembled_height",
               "Variant Metafield: dimensions.assembled_depth", "Variant Metafield: dimensions.assembled_weight", "Variant Metafield: dimensions.packaged_length",
               "Variant Metafield: dimensions.packaged_width", "Variant Metafield: dimensions.packaged_height", "Variant Metafield: dimensions.volume", ]
    
    def ProductToRow(product: Product) -> MatrixifyRow: 

        template = "pre-order" if product.preSale else ""
        
        if product.isVariant:
            mainImage = product.media.images[0] if product.media.images else None

            return MatrixifyRow(title=product.title, handle=product.handle, bodyHTML= product.HTMLDescription,vendor=product.brand, tags=product.tags, status=product.status, 
                                published=product.isPublished, publishedScope=product.publishedScope, images=product.media.images, variantSKU=product.sku, 
                                option1_name=product.variantProperties.option1.name,
                                option1_value=product.variantProperties.option1.value,
                                option2_name=product.variantProperties.option2.name,
                                option2_value=product.variantProperties.option2.value,
                                option3_name=product.variantProperties.option3.name,
                                option3_value=product.variantProperties.option3.value,
                                variantWeight=product.weight, variantBarcode= product.upc,
                                variantWeightUnit=product.weightUnit, variantImage=mainImage,inventoryPolicy=product.inventoryPolicy, v_meta_description=product.variant_description,
                                v_meta_includes=product.JSONIncludes, v_meta_applications=product.JSONApplications, v_meta_specs=product.JSONSpecifications,
                                v_meta_packQty=product.packQuantity, v_meta_videos=product.media.videos, v_meta_sds=product.resources.sds,
                                v_meta_tds=product.resources.tds, v_meta_specSheet=product.resources.specSheet, v_meta_moreInfoURL=product.resources.moreInfoURL,
                                v_meta_altResName=product.resources.alternateResource.name, v_meta_altResURL=product.resources.alternateResource.url, v_meta_modelNo=product.modelNo, 
                                meta_description=getTextFromHTML(product.HTMLDescription),v_meta_MPN=product.mfg_part_no, template=template, battery_system=product.battery_system,
                                assembled_length=product.dimensions.assembled_length, assembled_width=product.dimensions.assembled_width, assembled_height=product.dimensions.assembled_height,
                                assembled_depth=product.dimensions.assembled_depth, assembed_weight=product.dimensions.assembled_weight, packaged_length=product.dimensions.packaged_length,
                                packaged_width=product.dimensions.packaged_width, packaged_height=product.dimensions.packaged_height, volume=product.dimensions.volume)
        else:                       
            return MatrixifyRow(title=product.title, handle=product.handle, bodyHTML=product.HTMLDescription, vendor=product.brand, tags=product.tags, status=product.status, 
                                published=product.isPublished, publishedScope=product.publishedScope,images=product.media.images, variantSKU=product.sku, variantWeight=product.weight,
                                variantWeightUnit=product.weightUnit, v_meta_includes=product.JSONIncludes, v_meta_applications=product.JSONApplications, 
                                v_meta_specs=product.JSONSpecifications, v_meta_packQty=product.packQuantity, v_meta_videos=product.media.videos, v_meta_sds=product.resources.sds,
                                v_meta_tds=product.resources.tds, v_meta_specSheet=product.resources.specSheet, v_meta_moreInfoURL=product.resources.moreInfoURL, variantBarcode=product.upc,
                                v_meta_altResName=product.resources.alternateResource.name, v_meta_altResURL=product.resources.alternateResource.url, 
                                v_meta_modelNo=product.modelNo , v_meta_MPN=product.mfg_part_no, inventoryPolicy=product.inventoryPolicy, template=template, battery_system=product.battery_system,
                                assembled_length=product.dimensions.assembled_length, assembled_width=product.dimensions.assembled_width, assembled_height=product.dimensions.assembled_height,
                                assembled_depth=product.dimensions.assembled_depth, assembed_weight=product.dimensions.assembled_weight, packaged_length=product.dimensions.packaged_length,
                                packaged_width=product.dimensions.packaged_width, packaged_height=product.dimensions.packaged_height, volume=product.dimensions.volume)