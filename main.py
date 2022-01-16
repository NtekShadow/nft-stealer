# 14/01/2022
# Made by NtekShadow
# NFT Stealer (OpenSea)

import requests
import os
import json
import math
import json
import requests
from tqdm import tqdm
from tabulate import tabulate


textStart = r""" made by NtekShadow

         __ _         _             _           
        / _| |       | |           | |          
  _ __ | |_| |_   ___| |_ ___  __ _| | ___ _ __ 
 | '_ \|  _| __| / __| __/ _ \/ _` | |/ _ \ '__|
 | | | | | | |_  \__ \ ||  __/ (_| | |  __/ |   
 |_| |_|_|  \__| |___/\__\___|\__,_|_|\___|_|  
     
     
 Please choose an option:
     
 [1]: Download standard quality NFT 
 [2]: Download standard quality NFT + NFT JSON Data
 [3]: Download high quality NFT                 
 [4]: Download high quality NFT + NFT JSON Data 
 [5]: Download only NFT JSON Data

(not all nft's include a hq image so [3] and [4] could fail)
"""
tableStart = [[textStart]]
output = tabulate(tableStart, tablefmt='grid')

print(output)
option = int(input("  Enter Option Number: "))
CollectionName = input("  Input NFT collection Name: ").lower()
# Get information regarding collection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
collection = requests.get(f"https://api.opensea.io/api/v1/collection/{CollectionName}?format=json")
price = requests.get(f"https://api.coinbase.com/v2/prices/ETH-USD/spot", headers=headers)

if collection.status_code == 429:
    print("Server returned HTTP 429. Request was throttled. Please try again in about 5 minutes.")

if collection.status_code == 404:
    print("NFT Collection not found.\nPress ENTER to exit")
    input()
    exit()

collectioninfo = json.loads(collection.content.decode())
priceinfo = json.loads(price.content.decode())

# Create image folder if it doesn't exist.

if not os.path.exists('./images'):
    os.mkdir('./images')

if not os.path.exists(f'./images/{CollectionName}'):
    os.mkdir(f'./images/{CollectionName}')


    # Get total NFT count
    collectioninfo = json.loads(collection.content.decode())
    priceinfo = json.loads(
        requests.get(f"https://api.coinbase.com/v2/prices/ETH-USD/spot", headers=header).content.decode())
    count = int(collectioninfo["collection"]["stats"]["count"])
    eth_price = float(priceinfo["data"]["amount"])
    avg_price = float(collectioninfo["collection"]["stats"]["average_price"])

    # Opensea limits to 50 assets per API request, so last variable is the highest iteration needed.
    nft_stealer(option, collection_name, math.ceil(count / 50))

    est_stolen = stats["DownloadedImages"] * avg_price
    est_stolen_usd = stats["DownloadedImages"] * avg_price * eth_price

    table_end = [[f"""

    Finished downloading collection.
    Statistics
    -=-=-=-=-=-
    Total of {count} units in collection "{collection_name}".

    Money:
    ----------
    avg price: {avg_price} ♦

    Estimated stolen->
    ETH: {est_stolen:.2f} ♦
    USD: {est_stolen_usd:.2f} $

    Downloads:
    ----------
    Images ->
    successfully downloaded:    {stats["DownloadedImages"]}
    already downloaded:         {stats["AlreadyDownloadedImages"]}

    Data ->
    successfully downloaded:    {stats["DownloadedData"]}
    already downloaded:         {stats["AlreadyDownloadedData"]}  

    You can find the images in the images/{collection_name} folder.
    You can find the Data in the images/{collection_name}/data folder.
                               ___            
      /\  /\__ ___   _____    / __\   _ _ __  
     / /_/ / _` \ \ / / _ \  / _\| | | | '_ \ 
    / __  / (_| |\ V /  __/ / /  | |_| | | | |
    \/ /_/ \__,_| \_/ \___| \/    \__,_|_| |_|

    Press enter to exit..."""]]
    print(tabulate(table_end, tablefmt='grid'))
    input()


def nft_stealer(nft_option, collection_name, iterations):
    print(f"\n  Downloading collection {collection_name}:\n")
    for i in tqdm(range(iterations)):
        data = json.loads(requests.get(
            f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={i * 50}"
            f"&limit=50&collection={collection_name}&format=json", headers=header).content.decode())

        if "assets" in data:
            match nft_option:
                case "1":
                    nft_stealer_images(data, collection_name, False)
                case "2":
                    nft_stealer_images(data, collection_name, False)
                    nft_stealer_data(data, collection_name)
                case "3":
                    nft_stealer_images(data, collection_name, True)
                case "4":
                    nft_stealer_images(data, collection_name, True)
                    nft_stealer_data(data, collection_name)
                case "5":
                    nft_stealer_data(data, collection_name)
                case _:
                    print(f"{nft_option} is not a valid option.")
                    exit()
        else:
            break


def nft_stealer_images(data, collection_name, hq):
    for asset in data["assets"]:
        formatted_number = f"{int(asset['token_id']):04d}"
        if os.path.exists(f'./images/{collection_name}/{formatted_number}.png'):
            stats["AlreadyDownloadedImages"] += 1
        else:
            if hq and asset["image_original_url"]:
                image = requests.get(asset["image_original_url"])
            else:
                if asset["image_url"]:
                    image = requests.get(asset["image_url"])
                else:
                    continue
            if image.status_code == 200:
                file = open(f"./images/{collection_name}/{formatted_number}.png", "wb+")
                file.write(image.content)
                file.close()
                stats["DownloadedImages"] += 1
            else:
                image.raise_for_status()
                continue


def nft_stealer_data(data, collection_name):
    if not os.path.exists(f'./images/{collection_name}/data'):
        os.mkdir(f'./images/{collection_name}/data')
    for asset in data["assets"]:
        formatted_number = f"{int(asset['token_id']):04d}"
        if os.path.exists(f'./images/{collection_name}/data/{formatted_number}.json'):
            stats["AlreadyDownloadedData"] += 1
        else:
            file = open(f"./images/{collection_name}/data/{formatted_number}.json", "w+")
            json.dump(asset, file, indent=3)
            file.close()
            stats["DownloadedData"] += 1


if __name__ == '__main__':
    run_nft_stealer()
