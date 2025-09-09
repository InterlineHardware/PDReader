from src.Transformer import *
from src.ExcelProcesser import *
from src.Products import *
    
def dispatcher(objs: list):
    transformedObjects = []
    transformer = Transformer()
    for obj in objs:
        transformedObj = transformer.transform(obj)
        transformedObjects.append(transformedObj)
    return transformedObjects

#Main

if __name__ == "__main__":
#--------------Loading Spire products into memory-------------------------
    
    excelProcessor = PDProcessor("", "Product Data")
    listOfProducts: list = excelProcessor.readPDProducts(2, 19)

    #--------------Transformation into Product objects-------------------------
    transformed: list[Product] = dispatcher(listOfProducts)    #All products transformed


    excelProcessor.generateMatrixifyFile(transformed)

#===============================================================================================#
