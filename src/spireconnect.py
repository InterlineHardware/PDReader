import spyre
import src.Logline as Logline
from src.Products import PDRow
from spyre.Models.inventory_models import InventoryItem, ItemUDF
from typing import Dict

logger = Logline.Logger("SPIRE_CONNECTOR").logger

class spireConnector(spyre.Spire):
    """Handles Logic for converting PD Data to spyre records and uses spyreapi client library to process data into spyre"""  

    def check_upload(self, sku : str) -> bool:
        """
        Sets upload field of the sku to True
        Warehouse 00 used as default

        Args:
            sku (str): The SKU that needs to be checked upload
        
        Returns:
            bool: True if successfull
        """
        try:
            item = self.inventory.items.get_item(part_no=sku, warehouse="00")
            item = item.update(InventoryItem(upload=True))
            if item.model.upload:
                logger.info(f"Upload To web Checked For {sku}")
                return True
        except Exception as e :
            logger.warning(f"Error Checking upload for SKU : {sku} . ERROR : {e}")
            return False
        
    def false_tpo(self, sku : str) -> bool:
        """
        Sets the udf field, to_put_online of the sku to be false
        Warehouse 00 used as default

        Args:
            sku (str): The SKU that needs to be removed from to put online
        
        Returns:
            bool: True if successfull
        """
        try:
            item = self.inventory.items.get_item(part_no=sku, warehouse="00")
            item = item.update(InventoryItem(udf=ItemUDF(put_online=False)))
            if not item.model.udf.put_online:
                logger.info(f"TO PUT ONLINE Set to False For {sku}")
                return True
        except Exception as e:
            logger.warning(f"Error setting put_online to False for SKU : {sku} . Error : {e}")
            return False
        
    def pushProduct(self, PDRow : PDRow):
        """
        Pushes data to spire UDF fields from a PDRow object. 

        Args:
            PDRow (PDRow): The row to be pushed 
        
        Returns:
            bool: True if successfull
        """
        sku = PDRow.interline_sku
        item = self.inventory.items.get_item(part_no=sku, warehouse="00")
        payload = self.convertPDRowtoitem(PDRow)
        
        try:
            item.update(payload)
            logger.info(f"Product : {sku} PUSHED to SPIRE SUCCESsFULLY")
        except Exception as e:
            logger.error(f"Failed To Push Product : {sku} : Error : {e}")

    def convertPDRowtoitem(self, product: PDRow) -> Dict[str, dict]:
        """
        Converts a PDRow object into a dictionary payload suitable for 
        updating an inventory item in Spire ERP via the ItemUDF model.

        This function extracts product information from the PDRow instance 
        and maps it into the structure defined by the ItemUDF Pydantic model.
        
        Only non-null fields are included in the final output.

        Args:
            product (PDRow): The product data row to convert.

        Returns:
            Dict[str, dict]: A dictionary with the 'udf' key containing the
                            serialized user-defined fields for the inventory item.
        """
        udf = ItemUDF(
            desc=product.description,
            brand=product.brand,
            model=product.manufacturer_model_no,
            title=product.title,
            is_variant=product.isVariant,
            op1_name=product.variantProperties.option1.name if product.isVariant else None,
            op2_name=product.variantProperties.option2.name if product.isVariant else None,
            op3_name=product.variantProperties.option3.name if product.isVariant else None,
            op4_name=product.variantProperties.option4.name if product.isVariant else None,
            op1_value=product.variantProperties.option1.value if product.isVariant else None,
            op2_value=product.variantProperties.option2.value if product.isVariant else None,
            op3_value=product.variantProperties.option3.value if product.isVariant else None,
            op4_value=product.variantProperties.option4.value if product.isVariant else None,
            category1=product.category.c1,
            category2=product.category.c2,
            category3=product.category.c3,
            category4=product.category.c4,
            pk_qty=product.pack_quantity,
            features=product.concatenated_features,
            includes=product.concatenated_includes,
            applications=product.concatenated_applications,
            specifications=product.concatenated_specs,
            asm_depth=product.assembled_depth,
            asm_width=product.assembled_width,
            asm_height=product.assembled_height,
            asm_length=product.assembled_length,
            asm_weight=product.assembled_weight,
            asm_weight_op=product.assembled_operating_weight,
            pkg_depth=product.packaged_depth,
            pkg_width=product.packaged_width,
            pkg_height=product.packaged_height,
            pkg_length=product.packaged_length,
            pkg_weight=product.packaged_weight,
            volume=product.volume,
            image_urls=product.images,
            video_urls=product.videos,
            sds_url=product.resources.sds,
            tds_url=product.resources.tds,
            more_info_url=product.resources.moreInfoURL,
            specsheet_url=product.resources.specSheet,
            alternate_res=product.resources.alternateResource.name,
            alternate_res_src=product.resources.alternateResource.url,
            # Optional new UDF fields you may want to populate
            html_specs=None,
            html_includes=None,
            html_desc_feat=None,
            html_dimensions=None,
            html_applications=None,
            # Add other fields as necessary
        )

        return {"udf": udf.dict(exclude_none=True)}