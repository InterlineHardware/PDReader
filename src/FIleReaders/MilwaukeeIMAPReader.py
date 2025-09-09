import openpyxl
import src.Logline as Logline
from src.Models.PriceRecord import PriceRecord
from src.QueryModule import QueryModule
import src.processer as processer
import traceback


logger = Logline.Logger(__name__).logger

def openFile(excelfile):
    workbook = openpyxl.open(excelfile)
    logger.info("FILE OPENED")
    return workbook


def get_headers(sheet):
    header_row = sheet[2]  # Assuming headers are in the first row
    headers = {}
    for idx, cell in enumerate(header_row):
        if cell.value:  # Only add non-empty headers
            headers[cell.value] = idx
    return headers


def getPriceRecord(row, headers):
    modelno = row[headers["ITEM NO."]]
    description = row[headers["DESCRIPTION"]]
    sell_price = row[headers["2025 IMAP RETAIL"]] if "2025 IMAP RETAIL" in headers else row[headers["2024 IMAP RETAIL"]]

    priceRecord = PriceRecord(
        modelno=modelno, description=description, sell_price=sell_price
    )
    return priceRecord

def readsheet(workbook : openpyxl.Workbook, conn):
    logger.info("READING PRICE SHEET")
    priceSheet = workbook["EVERYDAY IMAP LIST"]
    queryModule = QueryModule(conn)
    # Create a dictionary to map header names to column indices
    header_indices = get_headers(priceSheet)

    for row in priceSheet.iter_rows(min_row=3, max_row=priceSheet.max_row, values_only=True):
        MFG_Part_Number = row[header_indices["ITEM NO."]]
        if MFG_Part_Number is None:
            continue
        try:
            priceRecord = getPriceRecord(row, header_indices)
            processer.priceRecordQuery(priceRecord, queryModule)
        except Exception as err:
            logger.error(f"ERROR READING PRICE SHEET: {err}")
            traceback.print_exc()
            exit(1)
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