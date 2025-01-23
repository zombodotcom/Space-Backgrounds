import requests

print(requests.get("https://www.star.nesdis.noaa.gov/goes/fulldisk_band.php?sat=G16&band=GEOCOLOR&length=36&dim=1").text)