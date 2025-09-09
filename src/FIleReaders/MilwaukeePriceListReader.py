import openpyxl
import src.Logline as Logline
from src.QueryModule import QueryModule
import src.processer as processer
from src.Models.PriceRecord import PriceRecord

logger = Logline.Logger(__name__).logger


def openFile(excelfile):
    workbook = openpyxl.open(excelfile)
    logger.info("FILE OPENED")
    return workbook


def get_headers(sheet):
    header_row = sheet[4]  # Assuming headers are in the first row
    headers = {}
    for idx, cell in enumerate(header_row):
        if cell.value:  # Only add non-empty headers
            headers[cell.value] = idx
    return headers


def getPriceRecord(row, headers):
    modelno = row[headers["Item"]]
    description = row[headers["Item Description"]]
    status = row[headers["Status"]]
    # order_qty = row[headers['Order Qty']]  # Assuming 'Order Qty' is the correct header name
    # uom = row[headers['UOM']]  # Assuming 'UOM' is the correct header name
    list_price = row[headers["List Price"]]

    priceRecord = PriceRecord(
        modelno=modelno, description=description, status=status, list_price=list_price
    )
    return priceRecord


def readsheet(workbook, conn):
    logger.info("READING PRICE SHEET")
    priceSheet = workbook["MET-EMP-STL Items Price List"]
    queryModule = QueryModule(conn)
    # Create a dictionary to map header names to column indices
    header_indices = get_headers(priceSheet)

    for row in priceSheet.iter_rows(min_row=5, max_row=10, values_only=True):
        MFG_Part_Number = row[header_indices["Item"]]
        if MFG_Part_Number is None:
            continue
        try:
            priceRecord = getPriceRecord(row, header_indices)
            processer.priceRecordQuery(priceRecord, queryModule)
        except Exception as err:
            logger.error(f"ERROR READING PRICE SHEET: {err}")
        print(
            "============================000000000000=============================  \n\n\n"
        )


def readFile(excelfile):
    Logline.LogData.startTimer()
    workbook = openFile(excelfile)
    conn = processer.connect()

    if conn is None or not conn.is_connected():
        logger.error("No Connection with Databse")
        return None

    readsheet(workbook, conn)
