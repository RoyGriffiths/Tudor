from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import sys

def OpenInterest():

    # Open the url, obtain the htm, get the text using Beautiful Soup, then split the lines:
    htm = urlopen("https://www.cftc.gov/dea/futures/deanymesf.htm")
    soup = BeautifulSoup(htm, "html.parser")
    text = soup.find("pre").text.splitlines()[4:]

    # Now we will loop through extracting the names and OI.
    # From inspection the contract name comes every 21 lines and the OI comes 7 after that.
    contractLine = 0
    OILine = contractLine + 7

    # A simple loop finding and formatting the text:
    print("contract, open_interest")
    while OILine < len(text):
        textStrip = text[contractLine].find(" - NEW YORK MERCANTILE EXCHANGE")
        contract = text[contractLine][:textStrip].strip()
        textStrip = text[OILine].find("OPEN INTEREST:")
        OI = text[OILine][textStrip+14:].strip()
        print(contract + ", " + OI)
        contractLine += 21
        OILine += 21

def extensionStats(filepath = "-1"):

    # If there is an input directory, use that, otherwise use current directory:
    if len(sys.argv) >= 2:
        filepath = str(sys.argv[1])
    elif filepath == "-1":
        filepath = os.getcwd()

    # Create lists to hold extension stats as well as extensions seen:
    stats = []
    extensionList = []

    # Loop through the files in the folder as well as sub-folders:
    for root, dirs, files in os.walk(filepath):
        for filename in files:

            # Get the file extension name as well as size:
            extension = os.path.splitext(filename)[1].lower()
            sizes = os.path.getsize(root + os.sep + filename)

            # Check if we have already seen this extension, if not add:
            if extension not in extensionList:
                extensionList.append(extension)
                stats.append([extension, 1, sizes, sizes])
                extensionList.sort()
                stats.sort()

            # Update the stats of the extension if we have seen before:
            else:
                index = extensionList.index(extension)
                stats[index][1] += 1
                if sizes > stats[index][2]:
                    stats[index][2] = sizes
                stats[index][3] += sizes

    # Formatting to print nicely:
    col_width = max(len(str(word)) for row in stats for word in row) + 1
    for row in stats:
        print("".join(str(word).ljust(col_width) for word in row))

if __name__ == '__main__':
    extensionStats()