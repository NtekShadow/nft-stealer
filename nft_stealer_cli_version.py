import os
import math
import json
import requests
from argparse import ArgumentParser


def run_nft_stealer(collection, image, quality, data):
	if not image and not data:
		print(f"Terminating program as both images and data arguments are set to False.")
		exit()

	header = {'User-Agent': 'Mozilla/5.0 (X11; Arch; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'}

	collection_data = requests.get(f"https://api.opensea.io/api/v1/collection/{collection}?format=json", headers=header)
	count = int(json.loads(collection_data.content.decode())["collection"]["stats"]["count"])

	if not collection_data.status_code == 200:
		collection_data.raise_for_status()
		exit()
	if not os.path.exists(f'./images'):
		os.mkdir(f'./images')
	if not os.path.exists(f'./images/{collection}'):
		os.mkdir(f'./images/{collection}')
	if not os.path.exists(f'./images/{collection}/data') and data:
		os.mkdir(f'./images/{collection}/data')

	for i in range(math.ceil(count / 50)):
		data_request = json.loads(requests.get(
			f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={i * 50}"
			f"&limit=50&collection={collection}&format=json", headers=header).content.decode())
		if image:
			for asset in data_request["assets"]:
				formatted_number = asset['token_id']
				if not os.path.exists(f"./images/{collection}/{formatted_number}.png"):
					if quality and asset["image_original_url"]:
						image_file = requests.get(asset["image_original_url"])
					else:
						if asset["image_url"]:
							image_file = requests.get(asset["image_url"])
						else:
							continue
					if image_file.status_code == 200:
						file = open(f"./images/{collection}/{formatted_number}.png", "wb+")
						file.write(image_file.content)
						file.close()
		if data:
			for asset in data_request["assets"]:
				formatted_number = f"{int(asset['token_id']):04d}"
				if not os.path.exists(f"./images/{collection}/data/{formatted_number}.json"):
					file = open(f"./images/{collection}/data/{formatted_number}.json", "w+")
					json.dump(asset, file, indent=3)
					file.close()

	print("Collection files downloaded.")


if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument("-c", "--collection", required=True, help="The collection tag", dest="collection")
	parser.add_argument("-i", "--images", action='store_true', help="Download images", dest="images")
	parser.add_argument("-q", "--quality", action='store_true', help="Prefer high quality", dest="quality")
	parser.add_argument("-d", "--data", action='store_true', help="Download JSON data", dest="data")
	parser = parser.parse_args()
	run_nft_stealer(parser.collection, parser.images, parser.quality, parser.data)
