import scrapy
import re
import pycountry
import uuid
from locations.items import GeojsonPointItem
from locations.categories import Code

class Serloinmexico(scrapy.Spider):
    name = "serloin_mexico_dac"
    brand_name = "SERLOIN_STOCKADE"
    spider_chain_id = "3562"
    spider_type = "chain"
    spider_categories = [Code.RESTAURANT]
    spider_countries = [pycountry.countries.lookup('mex').alpha_2]
    allowed_domains = ['sirloinmexico.com']
    start_urls =['http://sirloinmexico.com/sucursales/']

    def parse(self, response):
        # Extract the restaurant sections
        restaurant_divs = response.css('div[style*="width: 400px; float: left; margin: 10px 15px;"]')

        for restaurant_div in restaurant_divs:
            # Extract the restaurant name
            restaurant_name = restaurant_div.css('h3::text').get().strip()

            # Extract the address
            
            

            # Extract the phone numbers
            phone_numbers = restaurant_div.css('b::text').get().strip()
            opening_hours = restaurant_div.css('p::text').get().strip()
            
            # Extract script containing latlng information
            script_text = restaurant_div.css('script').extract_first()
            

            

            # Extract latlng variable information using regex
            latlng_matches = re.findall(r'new google.maps.LatLng\(([\d.-]+),\s*([\d.-]+)\);', script_text)
            if latlng_matches  :
                lat, lng = float(latlng_matches[0][0]), float(latlng_matches[0][1])
                
                

                # Create a GeojsonPointItem with the location information
                geojson_item = GeojsonPointItem(
                    ref= uuid.uuid4().hex,
                    name = restaurant_name,
                    brand="SERLOIN_STOCKADE",
                    chain_name="SERLOIN_STOCKADE",
                    chain_id="3562",
                    addr_full= "Mexico " + restaurant_name ,
                    country="Mexico",
                    city=restaurant_name,
                    phone=phone_numbers,
                    opening_hours=opening_hours,
                    website="http://sirloinmexico.com/sucursales/",
                    lon=lng,
                    lat=lat
                )

                # Yield the GeoJSON item
                yield geojson_item