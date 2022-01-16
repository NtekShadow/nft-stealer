# NFT Stealer
This executable lets you download all collections from https://opensea.io.

## Usage
Download the executable and Start it. (you can get it from releases: https://github.com/NtekShadow/nft-stealer/releases)
Alternatively you can run the pthon script directly.

A command Promt will pop up and ask you to enter an option and the target collection:

![alt text](https://github.com/NtekShadow/nft-stealer/blob/master/main/images/nft-stealer-one.png?raw=true)

after entering both of these valid just wait untill the programm finishes the download and get shown a box with statistics.

![alt text](https://github.com/NtekShadow/nft-stealer/blob/master/main/images/nft-stealer-two.png?raw=true)

## How does it work?
By using the Opensea API, setting an User-Agent and fetching the items in bunches of 50 and iterrating through the bunches untill all items are downloaded.
And by using the coinbase api getting the current price of ETH in USD for a little fun statistics. (wich is probably not accurat at all)

The image fetching is base of this repo: https://github.com/sj-dan/OpenSea-NFT-Stealer

## Why spend time making this?
NFT's are a joke and i saw the repo of @https://github.com/sj-dan/ and decided to make it way more user friendly and easy to use.
This way more people can easily let the right-click go brrr without knowledge in Python or a working programming enviroment.

## Known Issues:
  if choosing to download HQ Images, no images are downloaded at all:
  
   -Collection doenst provide HQ Image link
    
  Sometimes flagged by AntiVirus for bein a Trojan:
  
  -This is due to pyinstaller bundleing into one file. I have submitted the file to Avast and AVG for checking. Once they agree that it doenst contain a trojan, try updating the virus definitions in your anti virus software and that should stop the false positive. if its too insecure for you, you can run the python script directly
    
  High possibility of this code breaking if Opensea API changes something with their api
