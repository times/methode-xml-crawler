import requests
import sys
import os
from bs4 import BeautifulSoup
from pathlib import Path
import chalk
from config import config

# Definitions for filetypes for naming


def fileType(link):
    filetype = link.category.get("term")
    if filetype == "edition":
        return str(link.find("cpi:editiondate").text + "-" + link.find("dcterms:identifier").text.split("-")[0])
    if filetype == "puzzle":
        return str(link.find("cpi:puzzletype").text)
    elif filetype == "section":
        return str(link.title.text)
    elif filetype == "slot":
        return str(link.find("cpi:times_templateid").text + "-" + link.find("dcterms:identifier").text.split("-")[0])
    elif filetype == "book":
        return str(link.title.text)
    elif filetype == "images":
        return str(link.find("cpi:chpid").text)
    elif filetype == "article":
        return str(link.find("cpi:slug").text + "-" + link.find("dcterms:identifier").text.split("-")[0][0])
    else:
        return str(link.find("dcterms:identifier").text.split("-")[0])

# Main function


def writeFile(filepath: str, filelink: str, iteration: int, logLevel: int):

    # Fetch the link from HTTP, return as XML blob
    data = requests.get(filelink).text
    # Soupify XML blob
    soup = BeautifulSoup(data, features="html.parser")

    # Run fileType function to determine naming convention
    filetype = fileType(soup)

    # Build path from current path plus filetype
    path = filepath + "/" + filetype

    # Check depth limit
    depth = len(filepath.split("/"))
    if depth > config["maxDepth"]:
        return
    # Tell the console where we are
    if logLevel > 0:
        print(chalk.bold("Depth/Iteration: ") +
              chalk.blue(depth) + "/" + chalk.cyan(iteration))

    # Write the files
    if not os.path.exists(path + "/" + filetype + ".xml"):
        os.makedirs(path)
        f = open(path + "/" + filetype + ".xml", "w+")
        f.write(soup.prettify())
        f.close()
    # Get the next set of links
    for link in soup.find_all("link"):
        # Quits if file is a binary or would result in a image save
        if (link.get("cpi:qualifier") == "binary"):
            return
        if ".png" in link.get("href"):
            return
        if ".jpg" in soup.link.get("href"):
            return
        iteration = iteration + 1
        writeFile(path, link.get("href"), iteration, logLevel)


# Print out config
print(chalk.red("######"))
print(chalk.bold("Methode crawler"))
print(chalk.red("######"))
print(chalk.green("Depth: ") + chalk.white(config["maxDepth"]))
print("Logging level: " + str(config["logLevel"]))
# Run function
writeFile("output/", sys.argv[1], 0, config["logLevel"])
