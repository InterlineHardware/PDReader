import mysql.connector
from src.Logline import LogData, Logger
from src.Models.InventoryRecord import InventoryRecord
from src.Models.ProductDetailsRecord import ProductDetailsRecord
from src.Models.UOMRecord import UOMRecord
from src.Models.PriceRecord import PriceRecord


class QueryModule:
    logger = Logger("QueryMOD").logger

    # --------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------#
    # >> Queries

    InventoryINSERTQUERY = """
                        INSERT INTO inventory (
                            MFG_Part_Number, GTIN, Status, Short_Description, Show_Online_Date,
                            Available_to_Ship_Date, Brand, SubBrand, CountryCode, Warranty, Recalled,
                            ReplacementModelNo, PreviousModelNo, PreviousUPC, OrderUOM, MinOrder, MulOrder) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        );"""

    ProductDetailsINSERTQUERY = """
                            INSERT INTO ProductDetails (
                                modelno, inventory_id, search_keywords, product_name, description, features, includes, specs, images, video, sds,
                                AssembledLength, AssembledWidth, AssembledHeight, AssembledDepth, AssembledWeight, 
                                AssembledOperatingWeight, PackagedLength, PackagedWidth, 
                                PackagedHeight, PackagedDepth, PackagedWeight, Volume
                            ) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """

    UomINSERTQUERY = """
                            INSERT INTO uoms (mfg_part_no, `desc`, quantity, uom, upc, weight, width, depth, height, inventory_id) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """

    PriceINSERTQUERY = """
                            INSERT INTO PriceTable (
                                modelno, description, status, order_quantity, uom, list_price, inventory_id, sell_price
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                            """
    
    GETPRODUCTDATAQUERY = """
                            SELECT pd.modelno, pd.inventory_id, pd.search_keywords, pd.product_name, pd.description, 
                                pd.features, pd.includes, pd.specs, pd.images, pd.video, pd.sds, 
                                pd.AssembledLength, pd.AssembledWidth, pd.AssembledHeight, pd.AssembledDepth, 
                                pd.AssembledWeight, pd.AssembledOperatingWeight, pd.PackagedLength, 
                                pd.PackagedWidth, pd.PackagedHeight, pd.PackagedDepth, pd.PackagedWeight, 
                                pd.Volume, i.Show_Online_Date 
                            FROM ProductDetails pd
                            JOIN Inventory i ON pd.inventory_id = i.id  -- Join with Inventory table
                            WHERE pd.modelno = %s
                        """
    # --------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, connection: mysql.connector.MySQLConnection):
        self.conn = connection
        self.cursor = connection.cursor(buffered=True)

    def insertInventoryRecord(self, inventoryRecord: InventoryRecord):
        try:
            self.cursor.execute(
                self.InventoryINSERTQUERY, inventoryRecord.insertRecord()
            )
            self.conn.commit()
            # self.logger.info(f'Inserted Inventory record with MFG_Part_Number: {inventoryRecord.MFG_Part_Number}')
            LogData.addInventoryCount()
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error inserting Inventory record with MFG_Part_Number: {inventoryRecord.MFG_Part_Number}: {err}"
            )
            self.conn.rollback()

    def updateInventoryRecord(self, inventoryRecord: InventoryRecord):
        update_query, parameters = inventoryRecord.buildUpdateQuery()
        if not update_query:
            self.logger.info(
                f"No values to Update for: {inventoryRecord.MFG_Part_Number} "
            )
            return
        try:
            self.cursor.execute(update_query, parameters)
            self.conn.commit()
            # self.logger.info(f'Updated Inventory record with MFG_Part_Number: {inventoryRecord.MFG_Part_Number}')
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error updating Inventory record with MFG_Part_Number: {inventoryRecord.MFG_Part_Number}: {err}"
            )
            self.conn.rollback()

    def insertProductDetails(self, productDetails: ProductDetailsRecord):
        try:
            self.cursor.execute(
                self.ProductDetailsINSERTQUERY, productDetails.insertRecord()
            )
            self.conn.commit()
            # self.logger.info(f'Inserted ProductDetails record with modelno: {productDetails.modelno}')
            LogData.addProductDetailsCount()
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error inserting ProductDetails record with modelno: {productDetails.modelno}: {err}"
            )
            self.conn.rollback()

    def updateProductDetails(self, productDetails: ProductDetailsRecord):
        update_query, parameters = productDetails.buildUpdateQuery()
        if not update_query:
            self.logger.info(f"No values to Update for: {productDetails.modelno} ")
            return
        try:
            self.cursor.execute(update_query, parameters)
            self.conn.commit()
            # self.logger.info(f'Updated ProductDetails record with modelno: {productDetails.modelno}')
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error updating ProductDetails record with modelno: {productDetails.modelno}: {err}"
            )
            self.conn.rollback()

    def insertUOMRecord(self, uomRecord: UOMRecord):
        try:
            self.cursor.execute(self.UomINSERTQUERY, uomRecord.insertRecord())
            self.conn.commit()
            # self.logger.info(f"Inserted UOM record with MFG_Part_Number: {uomRecord.mfg_part_no} and UOM: {uomRecord.uom}")
            LogData.addUOMCount()
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error inserting UOM record with MFG_Part_Number: {uomRecord.mfg_part_no} and UOM: {uomRecord.uom}: {err}"
            )
            self.conn.rollback()

    def updateUOMRecord(self, uomRecord: UOMRecord):
        update_query, values = uomRecord.updateQuery()
        if not update_query:
            self.logger.info(
                f"No values to Update for: {uomRecord.mfg_part_no} and UOM: {uomRecord.uom}"
            )
            return
        try:
            self.cursor.execute(update_query, values)
            self.conn.commit()
            # self.logger.info(f"Updated UOM record with MFG_Part_Number: {uomRecord.mfg_part_no} and UOM: {uomRecord.uom}")
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error updating UOM record with MFG_Part_Number: {uomRecord.mfg_part_no} and UOM: {uomRecord.uom}: {err}"
            )
            self.conn.rollback()

    def insertPriceRecord(self, priceRecord: PriceRecord):
        try:
            self.cursor.execute(self.PriceINSERTQUERY, priceRecord.insertRecord())
            self.conn.commit()
            # self.logger.info(f'Inserted Price record with modelno: {priceRecord.modelno}')
            LogData.addPriceCount()
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error inserting Price record with modelno: {priceRecord.modelno}: {err}"
            )

    def updatePriceRecord(self, priceRecord: PriceRecord):
        update_query, parameters = priceRecord.buildUpdateQuery()
        if not update_query:
            self.logger.info(f"No values to update for: {priceRecord.modelno}")
            return
        try:
            self.cursor.execute(update_query, parameters)
            self.conn.commit()
            #
        except mysql.connector.Error as err:
            self.logger.error(
                f"Error updating Price record with modelno: {priceRecord.modelno}: {err}"
            )

    def inventoryRecordFetch(self, partnum):
        self.cursor.execute(
            "SELECT COUNT(*) FROM Inventory WHERE MFG_Part_Number = %s", (partnum,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def productDetailsRecordFetch(self, partnum):
        self.cursor.execute(
            "SELECT COUNT(*) FROM ProductDetails WHERE modelno = %s", (partnum,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def getInventoryID(self, partnum):
        self.cursor.execute(
            "SELECT id FROM inventory WHERE MFG_Part_Number = %s", (partnum,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def uomRecordFetch(self, inventoryID, uom):
        self.cursor.execute(
            "SELECT COUNT(*) FROM uoms WHERE inventory_id = %s AND uom = %s",
            (inventoryID, uom),
        )
        record = self.cursor.fetchone()
        if record:
            return record[0]
        return None

    def priceRecordFetch(self, inventoryID):
        self.cursor.execute(
            "SELECT COUNT(*) FROM PriceTable WHERE inventory_id = %s", (inventoryID,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def getProductDetails(self, modelno):
        try:
            self.cursor.execute(self.GETPRODUCTDATAQUERY, (modelno,))
            result = self.cursor.fetchone()
            if result:
                return result
        except Exception as err:
            self.logger.error(f"Could Not Find Model No in Database : {err}")

    