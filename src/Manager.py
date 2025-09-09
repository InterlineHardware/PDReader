from src.Dispatcher import dispatcher
import src.Logline as Logline
import src.Stage2Converter as Stage2Converter  
from src.ExcelProcesser import *
from src.spireconnect import spireConnector
import traceback
import src.processer as processer
import src.FIleReaders.ProductDataReader as pdReader
from src.Utilities import *
from spyre import SpireClient

logger = Logline.Logger(__name__).logger

class Manager:
    
    def __init__(self, company: str, username: str, password: str, host: str):
        spire_client = SpireClient(host=host,company=company,username=username,password=password,secure=False)
        self.spire_client = spireConnector(client= spire_client) 
    
    def convertToStage2(self, filePath, sheetName, specFormat, data):
        try:
            Stage2Converter.main(filePath, sheetName, specFormat,data)
        except Exception as err: 
            logger.error(f"Error Converting to Stage 2 : {err}")
            traceback.print_exc()
        
    def Matrxify(self, filepath, sheetName, minRow, maxRow):
        pdReader = PDProcessor(filepath, sheetName)
        listOfProducts: list = pdReader.readPDProducts(minRow, maxRow)
        transformed: list[Product] = dispatcher(listOfProducts)
        pdReader.generateMatrixifyFile(transformed)

    def CheckUpload(self,filePath, sheetName):
        SKUList = getSKUList(filePath,sheetName)
        for sku in SKUList:
            self.spire_client.check_upload(sku=sku)
    
    def ToPutOnline(self,filePath,sheetName):
        SKUList = getSKUList(filePath,sheetName)
        for sku in SKUList:
            self.spire_client.false_tpo(sku=sku)
    
    def pushtoSpire(self,filePath, sheetName, minRow, maxRow):
        pdReader = PDProcessor(filePath, sheetName)
        listOfProducts: list = pdReader.readPDProducts(minRow, maxRow)
        for product in listOfProducts:
            self.spire_client.pushProduct(PDRow=product)
        print("All Requests Completed")

    def processPD(self, filePath, sheetName, minRow, maxRow):
        pdReader.process(excelfile = filePath, SheetName=sheetName, min_row=minRow, max_row=maxRow)
    
    def uploadFiles(self,file, fileReader):
        print(f"Uploading file: {file}")
        processer.addFiletoDatabase(file, fileReader)
        log_data = Logline.LogData.getLogData()
        logger.info(log_data)
        return log_data
        

