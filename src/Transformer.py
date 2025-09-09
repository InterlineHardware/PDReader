from src.Utilities import *
from src.Products import *

class Transformer:

    # ->> Gets Staus Based On PD Columns Status and ISOnline. 
    def getStatus(self, productStaus : bool, isOnline : bool):
        if productStaus == True:
            status = "Active" if isOnline == True else "Draft"
        else:
            status = "Draft"
        return status
    
        #Generates the url handle based on the given string arguments
    def generateHandle(self, *strings) -> str:
        
        combined_string = '-'.join(strings)
        combined_string = combined_string.replace(' ', '-')
        combined_string = ''.join(char for char in combined_string if char.isalnum() or char == '-')
        combined_string = '-'.join(part for part in combined_string.split('-') if part)
        
        return combined_string
    
    def transformMediaStringToList(self, images_string: str) -> list:
        
        image_urls = images_string.split(',\n')

        # Strip any whitespace from each URL
        image_urls = [url.strip() for url in image_urls]
        # Remove any empty strings
        image_urls = [url for url in image_urls if url]
        
        # validated_urls = []
        # for url in image_urls:
        #     try:
        #         valid = validateURL(url)
        #         if valid:
        #             validated_urls.append(url)
        #     except ImageError as imageError:
        #         #Log this
        #         print(f"Image Invalid: {imageError}")
        #     except requests.RequestException as re:
        #         #log this
        #         print(f"Request Error: {re}")
        
        # return validated_urls
        
        return image_urls
        
        #Media Processor
    def processSpireMedia(self, images: str, videos: str) -> Media:
        
        #convert image and video strings into lists
        imageList = self.transformMediaStringToList(images)
        videoList = self.transformMediaStringToList(videos)
        return Media(imageList, videoList)

        #Tags from tags column, categoires and sku and modelno
    def getTags(self, product : PDRow):  
        
        Categorytags = product.category.convertToTags()
        tags = ''
        if Categorytags != '':
            tags+= Categorytags + ','
        
        # if product.manufacturer_model_no != "":
        #     tags += f"{product.manufacturer_model_no},"

        if product.tags != "":
            tags +=  product.tags + ","
        
        if product.preSale:
            tags+= 'pre-order' + ','

        return tags
    
    def modifydescription(self, Product : PDRow):
        ul_match = re.search(r'<ul.*?</ul>', Product.html_desc_features, re.DOTALL)

        # If a <ul> is found, extract it, remove it from bodyHTML, and add it to variant_meta_description
        if ul_match:
            ul_content = ul_match.group(0)  # Extract the <ul> block
            Product.html_desc_features = Product.html_desc_features.replace(ul_content, "").strip()  # Remove the <ul> block from bodyHTML
            Product.variant_description += ul_content  # Append the <ul> block to variant_meta_description


    def transform(self, product: PDRow) -> Product:
        print("Transforming: " + product.interline_sku)
        
        #isOnline converted to Matrixify status
        status: str = self.getStatus(product.status, product.is_online)   #isOnline converted to Matrixify status
        
        #Handle generation
        if product.isVariant:
            handle: str = self.generateHandle(product.title)
        else:
            if product.manufacturer_model_no != "":
                handle: str =  self.generateHandle(product.manufacturer_model_no, product.title)
            else:
                handle: str =  self.generateHandle(product.interline_sku, product.title)
        
        #Pack Quantity
        packQuantity = product.pack_quantity if product.pack_quantity != "" else None

        #Images & Videos
        media = self.processSpireMedia(product.images, product.videos)

        #Weight
        weight = ""
        weightUnit = ""
        if product.packaged_weight != "":
            weight = getWeightFromString(product.packaged_weight)
            weightUnit = getWeightUnitFromString(product.packaged_weight)
        elif product.assembled_weight != "":
            weight = getWeightFromString(product.assembled_weight)
            weightUnit = getWeightUnitFromString(product.assembled_weight)
        
        if product.preSale:
            product.inventoryPolicy = 'continue'

        #tags
        tags = self.getTags(product)

        batter_system = ""
        if product.battery_system.strip() != "":
            elements = [elem.strip() for elem in product.battery_system.split(",") if elem.strip()]
            batter_system = f"[{', '.join(f'\"{e}\"' for e in elements)}]"
        
        if product.isVariant:
            if product.variant_description != '':
                features = None
                if product.concatenated_features != '':
                    features = product.concatenated_features.splitlines()
                product.variant_description = getRichTextDescription(desc=product.variant_description, features=features)
                product.html_desc_features != ''


        dimensions = Dimensions(product.assembled_length, product.assembled_width, product.assembled_height, product.assembled_depth, product.assembled_weight,
                                product.packaged_length, product.packaged_width, product.packaged_height, product.packaged_depth, product.volume)
        #Product Instantiation
        transformedProduct = Product(product.interline_sku, product.manufacturer_model_no, product.manufacturer_part_no, product.brand, product.title, product.category, 
                                     product.html_desc_features, status, weight, weightUnit, handle, packQuantity, product.upc, tags ,product.json_applications, 
                                     product.json_specs, product.json_includes, dimensions, product.resources, media, product.isVariant, 
                                     product.variantProperties,product.preSale, product.inventoryPolicy, product.variant_description, batter_system)
            
        return transformedProduct
    
    