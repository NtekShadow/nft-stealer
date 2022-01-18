# NFT Stealer
This executable lets you download all collections from https://opensea.io.

## Usage
Download the executable and Start it. (you can get it from releases: https://github.com/NtekShadow/nft-stealer/releases)
Alternatively you can run the python script directly.

A command prompt will pop up and ask you to enter an option and the target collection:

![alt text](https://github.com/NtekShadow/nft-stealer/blob/master/main/images/nft-stealer-one.png?raw=true)

after entering both of these valid just wait until the program finishes the download and get shown a box with statistics.

![alt text](https://github.com/NtekShadow/nft-stealer/blob/master/main/images/nft-stealer-two.png?raw=true)

## How does it work?
By using the Opensea API, setting a User-Agent and fetching the items in bunches of 50 and iterating through the bunches until all items are downloaded.
And by using the coinbase api getting the current price of ETH in USD for a little fun statistics. (which is probably not accurate at all)

## Known Issues:
  if choosing to download HQ Images, no images are downloaded at all:
  
   -Collection doesn't provide HQ Image link
    
  Sometimes flagged by AntiVirus for bein a Trojan/Not opening at all:
  
  -This is due to pyinstaller compressing into one file. I have submitted the file to Avast and AVG for checking. Once they agree that it doesn't contain a trojan, try updating the virus definitions in your antivirus software and that should stop the false positive. if it's too insecure for you, you can run the python script directly.
    
  High possibility of this code breaking if Opensea API changes something with their api
