import mysql.connector
from src.Logline import LogData, Logger
import src.FIleReaders.MilwaukeeIMAPReader as MilwaukeeIMAPReader
from src.QueryModule import QueryModule
from src.Models.InventoryRecord import InventoryRecord
from src.Models.ProductDetailsRecord import ProductDetailsRecord
from src.Models.UOMRecord import UOMRecord
import src.FIleReaders.MilwaukeeFileReader as MilwaukeeFileReader
from src.Models.PriceRecord import PriceRecord
import src.FIleReaders.MilwaukeePriceListReader as MilwaukeePriceListReader
from src.Models.Product import PDRow
from src.FIleReaders import ProductDataReader 
import shutil
import os

logger = Logger("Processer").logger


# --------------------------------------------------------------------------------------------------------------------------#
# Logic For what queary to run.
# Creates if new SKU, Updates if existing


def inventoryQuery(inventoryRecord: InventoryRecord, queryModule: QueryModule):
    exists = queryModule.inventoryRecordFetch(inventoryRecord.MFG_Part_Number)
    if exists:
        queryModule.updateInventoryRecord(inventoryRecord)  # Update existing record
    else:
        queryModule.insertInventoryRecord(inventoryRecord)  # insert inventory record


def productInfoQuery(
    productDetailsRecord: ProductDetailsRecord, queryModule: QueryModule
):
    # checks if the model number exists in prouduct details and inventory
    exists = queryModule.productDetailsRecordFetch(productDetailsRecord.modelno)
    inventoryID = queryModule.getInventoryID(productDetailsRecord.modelno)

    if inventoryID:
        productDetailsRecord.inventory_id = inventoryID  # get inventory ID
        if exists:
            queryModule.updateProductDetails(
                productDetailsRecord
            )  # if exists in product deatils update record
        else:
            queryModule.insertProductDetails(
                productDetailsRecord
            )  # else insert new record

    else:
        queryModule.insertInventoryRecord(
            InventoryRecord(productDetailsRecord.modelno)
        )  # if not int inventory creates new inventory record
        inventoryID = queryModule.getInventoryID(productDetailsRecord.modelno)
        productDetailsRecord.inventory_id = inventoryID
        logger.warning(f"NEW INVENTORY RECORD CREATED : {productDetailsRecord.modelno}")
        queryModule.insertProductDetails(productDetailsRecord)


def UOMquery(uomRecord: UOMRecord, queryModule: QueryModule):
    inventoryID = queryModule.getInventoryID(uomRecord.mfg_part_no)
    exists = queryModule.uomRecordFetch(inventoryID, uomRecord.uom)
    if inventoryID:
        if exists:
            queryModule.updateUOMRecord(uomRecord)
        else:
            uomRecord.inventory_id = inventoryID
            queryModule.insertUOMRecord(uomRecord)
    else:
        queryModule.insertInventoryRecord(InventoryRecord(uomRecord.mfg_part_no))
        inventoryID = queryModule.getInventoryID(uomRecord.mfg_part_no)
        uomRecord.inventory_id = inventoryID
        logger.warning(f"NEW INVENTORY RECORD CREATED : {uomRecord.mfg_part_no}")
        queryModule.insertUOMRecord(uomRecord)


def priceRecordQuery(priceRecord: PriceRecord, queryModule: QueryModule):
    inventoryID = queryModule.getInventoryID(priceRecord.modelno)

    if inventoryID:
        priceRecord.inventory_id = inventoryID
        # Check if the record exists in the PriceTable
        exists = queryModule.priceRecordFetch(inventoryID)
        if exists:
            queryModule.updatePriceRecord(priceRecord)
        else:
            queryModule.insertPriceRecord(priceRecord)
    else:
        queryModule.insertInventoryRecord(InventoryRecord(priceRecord.modelno))
        inventoryID = queryModule.getInventoryID(priceRecord.modelno)
        priceRecord.inventory_id = inventoryID
        logger.warning(f"NEW INVENTORY RECORD CREATED : {priceRecord.modelno}")
        queryModule.insertPriceRecord(priceRecord)


# -------------------------------------------------------------------------------------------------------------- #


def connect():
    try:
        conn = mysql.connector.connect(
            user="sanjid",
            password="sanjid1",
            host="192.168.0.10",
            database="productdata",
        )
        return conn
    except (mysql.connector.Error, IOError) as err:
        logger.info("Failed to connect: %s", err)
        return None


# >> Gets ProductInfo From ProductDetailsDatabase
# >> Returns a PD Row object
def getProduct(modelNo, queryModule: QueryModule):
    # Query the database for the product details
    product = queryModule.getProductDetails(modelNo)

    if product:
        # Unpack the product details, including the new Show_Online_Date
        (
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
            assembled_length,
            assembled_width,
            assembled_height,
            assembled_depth,
            assembled_weight,
            assembled_operating_weight,
            packaged_length,
            packaged_width,
            packaged_height,
            packaged_depth,
            packaged_weight,
            volume,
            show_online_date,  # New field for Show_Online_Date
        ) = product

        # Create a PDRow object with all details including sell_price and show_online_date
        pdRow = PDRow(
            modelno=modelno,
            inventory_id=inventory_id,
            search_keywords=search_keywords,
            product_name=product_name,
            description=description,
            features=features,
            includes=includes,
            specs=specs,
            images=images,
            video=video,
            sds=sds,
            assembled_length=assembled_length,
            assembled_width=assembled_width,
            assembled_height=assembled_height,
            assembled_depth=assembled_depth,
            assembled_weight=assembled_weight,
            assembled_operating_weight=assembled_operating_weight,
            packaged_length=packaged_length,
            packaged_width=packaged_width,
            packaged_height=packaged_height,
            packaged_depth=packaged_depth,
            packaged_weight=packaged_weight,
            volume=volume,
            show_online_date=show_online_date  # New field
        )

        print(show_online_date)
        return pdRow
    else:
        print("No Product Found")
        return None


# >> Selects FileReader From Chosen File Type


def addFiletoDatabase(excelfile, fileReader):
    if fileReader == "Milwaukee Product Information":
        MilwaukeeFileReader.readFile(excelfile)
    elif fileReader == "Milwaukee Price List":
        MilwaukeePriceListReader.readFile(excelfile)
    elif fileReader == "Milwaukee IMAP":
        MilwaukeeIMAPReader.readFile(excelfile)       

    os.makedirs("Uploaded Files", exist_ok=True)
    shutil.copy(excelfile, 'Uploaded Files')

