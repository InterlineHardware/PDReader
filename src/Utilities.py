import re
import requests
from bs4 import BeautifulSoup
import json
import openpyxl
import os, json

CONFIG_FILE = "config.json"


class Category():
    def __init__(self, cat_1="", cat_2="", cat_3="", cat_4=""):
        self.c1 = cat_1
        self.c2 = cat_2
        self.c3 = cat_3
        self.c4 = cat_4
        
    def __str__(self) -> str:
        return f"{self.c1} > {self.c2} > {self.c3} > {self.c4}"
    
    def convertToTags(self) -> str:
        string = self.c1
        if self.c2 != "":
            string += f",{self.c2}"
            if self.c3 != "":
                string += f",{self.c3}"
                if self.c4 != "":
                    string += f",{self.c4}"
        return string

class AlternateResource():

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
        
    def __str__(self) -> str:
        return f"\tAlternate Resource Name: {self.name}\n\tAlternate Resource Value: {self.url}"

class Media():

    def __init__(self, images: list=[], videos: list=[]):
        self.images = images
        self.videos = videos
        
    def __str__(self) -> str:
        return f"\tImages:\n\t{self.images}\n\tVideos: {self.videos}"

class Resources():

    def __init__(self, sds="", tds="", spec_sheet="", more_info="", alternate_res_name="", alternate_res_value=""):
        self.sds = sds if sds != "" else ""
        self.tds = tds if tds != "" else ""
        self.specSheet = spec_sheet if spec_sheet != "" else ""
        self.moreInfoURL = more_info if more_info != "" else ""
        self.alternateResource = AlternateResource(alternate_res_name, alternate_res_value)
        
    def __str__(self) -> str:
        return f"""\tSDS: {self.sds}\n\tTDS: {self.tds}\n\tSpec Sheet: {self.specSheet}\n\tMore Info: {self.moreInfoURL}\n{self.alternateResource}"""

class Option():

    def __init__(self, name="", value=""):
        self.name = name
        self.value = value
        
    def __str__(self) -> str:
        return f"{self.name} : {self.value}"

class Variant():

    def __init__(self, op1_name, op1_value, op2_name, op2_value, op3_name, op3_value, op4_name, op4_value, variantID=None):
        self.variantID = variantID
        self.option1 = Option(op1_name, op1_value)
        self.option2 = Option(op2_name, op2_value)
        self.option3 = Option(op3_name, op3_value)
        self.option4 = Option(op4_name, op4_value)
        
    def __str__(self) -> str:
        return f"\t{self.option1}\n\t{self.option2}\n\t{self.option3}\n\t{self.option4}"

class ImageError(Exception):
    

    def __init__(self, error) -> None:
        self.error = error
        super().__init__(f"Invalid URL: {error}")

class Dimensions():

    def __init__(self, assembeld_length, assembled_width, assembled_height, assembled_depth, assembled_weight, 
                 packaged_length, packaged_width, packaged_height, packaged_depth, volume):
        
        self.assembled_weight = self.getWeightJSON(assembled_weight)
        self.assembled_length = self.getdimemsionJSON(assembeld_length)
        self.assembled_depth = self.getdimemsionJSON(assembled_depth)
        self.assembled_width = self.getdimemsionJSON(assembled_width)
        self.assembled_height = self.getdimemsionJSON(assembled_height)

        self.packaged_length = self.getdimemsionJSON(packaged_length) if packaged_length != '' else self.getdimemsionJSON(packaged_depth)
        self.packaged_width = self.getdimemsionJSON(packaged_width) if packaged_width != '' else self.getdimemsionJSON(packaged_depth)
        self.packaged_height = self.getdimemsionJSON(packaged_height) if packaged_height != '' else self.getdimemsionJSON(packaged_depth)
        self.volume = self.getVolumeJSON(volume)

    def __str__(self) -> str:
       return (
            f"Dimensions:\n"
            f"\tAssembled Length: {self.assembled_length}\n"
            f"\tAssembled Width: {self.assembled_width}\n"
            f"\tAssembled Height: {self.assembled_height}\n"
            f"\tAssembled Depth: {self.assembled_depth}\n"
            f"\tAssembled Weight: {self.assembled_weight}\n"
            f"\tPackaged Length: {self.packaged_length}\n"
            f"\tPackaged Width: {self.packaged_width}\n"
            f"\tPackaged Height: {self.packaged_height}\n"
            f"\tVolume: {self.volume}"
        )
    
    def getWeightJSON(self, weight : str) -> str:

        value  = getWeightFromString(weight)
        unit = getWeightUnitFromString(weight)

        if not value or not unit:
            return None
        return json.dumps({"value" : value, "unit" : unit})

    def getdimemsionJSON(self, dim : str) -> str:
        pattern = r"(\d+(\.\d+)?\s?[a-zA-Z\"']+[0-9\u00B2\u00B3\u00B9]*)"
        dimensionUnits = {"in", "ft", "yd", "mm", "cm", "m"}
        dim_unit_mapping = {
        'inches': 'in', "'": 'ft', '""': "in", '"': "in" , "''": "in"
        }
        
        match = re.search(pattern, dim)
        if match:
            value = re.search(r"[\d.]+", match.group()).group()  # Extract the numeric value
            unit = re.search(r"[a-zA-Z\"']+[0-9\u00B2\u00B3\u00B9]*", match.group()).group()

            if unit.lower() in dimensionUnits:
                return  json.dumps({"value" : value, "unit" : unit.lower()})
            elif unit.lower() in dim_unit_mapping:
                return  json.dumps({"value" : value, "unit" :dim_unit_mapping.get(unit.lower())})
        else: 
            return None           

    def getVolumeJSON(self, volume : str) -> str:
        pattern = r"(\d+(\.\d+)?\s?[a-zA-Z\"']+[0-9\u00B2\u00B3\u00B9]*)"
        volumeUnits = { "ml", "cl", "l", "m3", "us_fl_oz", "us_pt", "us_qt", "us_gal", "imp_fl_oz", "imp_pt", "imp_qt", "imp_gal"}
        volume_unit_mapping = {
        'liter': 'l','gallon': 'us_gal',
        'gal': 'us_gal', 'qt': 'us_qt', 'fl oz' : 'us_fl_oz', 'fl' :'us_fl_oz', 'oz' : 'us_fl_oz',  
        }
        
        match = re.search(pattern, volume)
        if match:
            value = re.search(r"[\d.]+", match.group()).group()  # Extract the numeric value
            unit = re.search(r"[a-zA-Z\"']+[0-9\u00B2\u00B3\u00B9]*", match.group()).group()

            if unit.lower() in volumeUnits:
                return  json.dumps({"value" : value, "unit" : unit.lower()})
            elif unit.lower() in volume_unit_mapping:
                return  json.dumps({"value" : value, "unit" :volume_unit_mapping.get(unit.lower())})
        else: 
            
            return None            
        
def getWeightFromString(spireAssembledWeight: str) -> float:
    #Function to extract the numeric value of a weight string
    #Eg. "5.36lbs" -> 5.36

    # Regular expression pattern to match a floating-point number
    pattern = r'[-+]?\d*\.\d+|\d+'
    
    # Search for the pattern in the string
    match = re.search(pattern, spireAssembledWeight)
    
    if match:
        # Extract the matched numeric value
        numeric_value = float(match.group())
        return numeric_value
    else:
        return None  # No numeric value found in the string
    
def getWeightUnitFromString(spireAssembledWeight) -> str:

    if not spireAssembledWeight:
        return ""
    # Regular expression pattern to match alphabetic characters
    pattern = r'[a-zA-Z]+'
    
    # Search for the pattern in the string
    match = re.search(pattern, spireAssembledWeight)
    
    if match:
        # Extract the matched alphabetic characters
        alphabetic_chars = match.group()
        if "lb" in alphabetic_chars.lower() or "lbs" in alphabetic_chars.lower():
            return "lb"
        elif "kg" in alphabetic_chars.lower():
            return "kg"
        elif "oz" in alphabetic_chars.lower():
            return "oz"
        elif alphabetic_chars == "g":
            return "g"
        else:
            raise ValueError("The weight unit does not match one of the following types: lb, kg, oz, g")
    else:
        raise Exception("The weight string provided does not match regex\nInput String: " + spireAssembledWeight)  # No alphabetic characters found in the string
    
def validateURL(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return True
    else:
        raise ImageError()
    
def getTextFromHTML(html):
    # Parse the HTML content
    if not html:
        return ''
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the text, stripping extra whitespace
    lines = soup.get_text(separator='\n', strip=True)
    return lines

def getRichTextDescription(desc :str = None, features : list = None):
    """ Reutrns a JSON String Object Representing The Rich Text Structure"""

    if not desc and not features:
        return ""
    base_json = {
        "type": "root",
        "children": [
            
        ]
    }

    if desc:
        para_child =   {    "type": "paragraph",
                            "children": [ ]
                        }
        base_json["children"].append(para_child)

        paras = desc.split("\n\n")
        
        for para in paras:
            child = {
                "type" : "text",
                "value" : para
            }
            base_json["children"][0]["children"].append(child)


    if features:
        bullet_child =  {   "listType": "unordered",
                            "type": "list",
                            "children": [ ] 
                        }
        base_json["children"].append(bullet_child)

        for bullet in features:
            child = {
                "type": "list-item",
                "children": [
                    {
                        "type": "text",
                        "value": bullet
                    }
                ]
            }
            
            base_json["children"][-1]["children"].append(child)
        
    return json.dumps(base_json)

def getSKUList(excelfile, sheetName):

    """
    Returns a list of SKU from a PD Sheet, where SKU is in the First Column
    """
    workbook = openpyxl.load_workbook(excelfile)
    sheet = workbook[sheetName]
    SKUList= []
    for row in sheet.iter_rows(min_col=1, max_col=1, min_row=2, values_only=True):
        value = row[0]
        if value is not None and value != '':
            SKUList.append(value.strip())
    return SKUList

def save_config(data: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}