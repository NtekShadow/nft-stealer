# 14/01/2022
# Made by NtekShadow
# NFT Stealer (OpenSea)

import requests
import os
import json
import math
from past.builtins import raw_input
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

count = int(collectioninfo["collection"]["stats"]["count"])
eth_price = float(priceinfo["data"]["amount"])
avg_price = float(collectioninfo["collection"]["stats"]["average_price"])

# Opensea limits to 50 assets per API request, so here we do the division and round up.
iterations = math.ceil(count / 50)
# Define variables for statistics

stats = {
    "DownloadedImages": 0,
    "AlreadyDownloadedImages": 0,
    "FailedImages": 0,
    "AlreadyDownloadedData": 0,
    "DownloadedData": 0,
}


def nft_stealer_option(nft_option):
    if nft_option == 1:
        print(f"\n  Starting download of NFT collection {CollectionName} in normal Quality:\n")
        for i in tqdm(range(iterations)):
            offset = i * 50
            data = json.loads(requests.get(
                f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}"
                f"&limit=50&collection={CollectionName}&format=json", headers=headers).content.decode())
            nft_stealer_images(data)

    elif nft_option == 3:
        print(f"\n  Starting download of NFT collection {CollectionName} in High Quality:\n")
        for i in tqdm(range(iterations)):
            offset = i * 50
            data = json.loads(requests.get(
                f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}"
                f"&limit=50&collection={CollectionName}&format=json", headers=headers).content.decode())
            nft_stealer_images_hq(data)

    elif nft_option == 2:
        print(f"\n  Starting download of NFT collection {CollectionName} in normal Quality + NFT JSON DATA:\n")
        for i in tqdm(range(iterations)):
            offset = i * 50
            data = json.loads(requests.get(
                f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}"
                f"&limit=50&collection={CollectionName}&format=json", headers=headers).content.decode())
            nft_stealer_images(data)
            nft_stealer_data(data)

    elif nft_option == 4:
        print(f"\n  Starting download of NFT collection {CollectionName} in High Quality + NFT JSON DATA:\n")
        for i in tqdm(range(iterations)):
            offset = i * 50
            data = json.loads(requests.get(
                f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}"
                f"&limit=50&collection={CollectionName}&format=json", headers=headers).content.decode())
            nft_stealer_images_hq(data)
            nft_stealer_data(data)

    elif nft_option == 5:
        print(f"\n  Starting download of NFT collection {CollectionName} NFT JSON DATA:\n")
        for i in tqdm(range(iterations)):
            offset = i * 50
            data = json.loads(requests.get(
                f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}"
                f"&limit=50&collection={CollectionName}&format=json", headers=headers).content.decode())
            nft_stealer_data(data)
    else:
        nft_option = int(input(f"{nft_option} is not a valid option, try again:"))
        if 0 <= nft_option <= 5:
            nft_stealer_option(nft_option)
        else:
            print(f"{nft_option} is not a valid option, press ENTER to exit:")
            input()
            exit()


def nft_stealer_images(data):
    if not data is None:
        if "assets" in data:
            for asset in data["assets"]:
                formatted_number = f"{int(asset['token_id']):04d}"

                # Check if image already exists, if it does, skip saving it
                if os.path.exists(f'./images/{CollectionName}/{formatted_number}.png'):
                    stats["AlreadyDownloadedImages"] += 1
                else:
                    # Make the request to the URL to get the image
                    if not asset["image_url"] is None:
                        image = requests.get(asset["image_url"])
                    else:
                        continue

                    # If the URL returns status code "200 Successful", save the image into the "images" folder.
                    if image.status_code == 200:
                        file = open(f"./images/{CollectionName}/{formatted_number}.png", "wb+")
                        file.write(image.content)
                        file.close()
                        stats["DownloadedImages"] += 1
                    # If the URL returns a status code other than "200 Successful", alert the user and don't save the
                    # image
                    else:
                        continue


def nft_stealer_images_hq(data):
    if not data is None:
        if "assets" in data:
            for asset in data["assets"]:
                formatted_number = f"{int(asset['token_id']):04d}"

                # Check if image already exists, if it does, skip saving it
                if os.path.exists(f'./images/{CollectionName}/{formatted_number}.png'):
                    stats["AlreadyDownloadedImages"] += 1
                else:
                    # Make the request to the URL to get the image
                    if not asset["image_original_url"] == None:
                        image = requests.get(asset["image_original_url"])
                    else:
                        if not asset["image_url"] == None:
                            image = requests.get(asset["image_url"])
                        else:
                            continue
                        # If the URL returns status code "200 Successful", save the image into the "images" folder.
                        if image.status_code == 200:
                            file = open(f"./images/{CollectionName}/{formatted_number}.png", "wb+")
                            file.write(image.content)
                            file.close()
                            stats["DownloadedImages"] += 1
                        # If the URL returns a status code other than "200 Successful", alert the user and don't save
                        # the image
                        else:
                            continue


def nft_stealer_data(data):
    if not os.path.exists(f'./images/{CollectionName}/image_data'):
        os.mkdir(f'./images/{CollectionName}/image_data')
    if not data is None:
        if "assets" in data:
            for asset in data["assets"]:
                formatted_number = f"{int(asset['token_id']):04d}"

                if os.path.exists(f'./images/{CollectionName}/image_data/{formatted_number}.json'):
                    stats["AlreadyDownloadedData"] += 1
                else:
                    # Take the JSON from the URL, and dump it to the respective file.
                    file = open(f"./images/{CollectionName}/image_data/{formatted_number}.json", "w+")
                    json.dump(asset, file, indent=3)
                    file.close()
                    stats["DownloadedData"] += 1

nft_stealer_option(option)

estm_stolen = stats["DownloadedImages"] * avg_price
estm_stolen_usd = estm_stolen * eth_price

textEnd = f"""

Finished downloading collection.
Statistics
-=-=-=-=-=-
Total of {count} units in collection "{CollectionName}".

Money:
----------
avg price: {avg_price} ♦

Estimated stolen->
ETH: {estm_stolen:.2f} ♦
USD: {estm_stolen_usd:.2f} $

Downloads:
----------
Images ->
successfully downloaded:    {stats["DownloadedImages"]}
already downloaded:         {stats["AlreadyDownloadedImages"]}

Data ->
successfully downloaded:    {stats["DownloadedData"]}
already downloaded:         {stats["AlreadyDownloadedData"]}  
    
You can find the images in the images/{CollectionName} folder.
You can find the Data in the images/{CollectionName}/data folder.
                           ___            
  /\  /\__ ___   _____    / __\   _ _ __  
 / /_/ / _` \ \ / / _ \  / _\| | | | '_ \ 
/ __  / (_| |\ V /  __/ / /  | |_| | | | |
\/ /_/ \__,_| \_/ \___| \/    \__,_|_| |_|

Press enter to exit..."""
tableEnd = [[textEnd]]
output = tabulate(tableEnd, tablefmt='grid')
print(output)
raw_input()

