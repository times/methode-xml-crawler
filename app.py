import requests
import sys
import os
from bs4 import BeautifulSoup
from pathlib import Path

def writeFile (filepath: str, filelink, iteration):
        if "/" in filelink.get('href'):
            filename = filelink.get("href").split('/')[-1].split('-')[0]
        else:
            filename = filelink
        print(iteration, filename)
        if ".jpg" in filename:
            print('quit jpg')
            return
        filedata = BeautifulSoup(requests.get(filelink.get('href')).text, features="html.parser")
        filetype = filedata.category.get('term')
        path = filepath + "/" + filename
        depth = filepath.split("/")
        if len(depth) < 7:
            if not os.path.exists(filepath + "/" + filetype + "-" + filename + ".xml"):
                os.makedirs(path)
                f = open(filepath + "/" + filetype + "-" + filename + ".xml", "w+")
                f.write(filedata.prettify())
                f.close()
            for link in filedata.find_all('link'):
                # if iteration == 5:
                #     return
                # else:
                if (link.get("cpi:qualifier") != "binary"):
                    if (".png" not in link.get("href")):
                        iteration = iteration + 1
                        writeFile(path, link, iteration)
                    else:
                        return
                else:
                    print("binary")
                    return
        else:
            print("depth limit reached")
            print(depth)
            print(path)
            return

firstFile = BeautifulSoup(requests.get(sys.argv[1]).text, features="html.parser").link
originalPath = "output/" + sys.argv[1].split("/")[-1].split("&")[0]

# # print("Firstfile", firstFile.link.get('href'))
# # print("first",firstFile.link.get('href'))


# if Path(path).exists() == False:
#     os.makedirs(path)

writeFile(originalPath, firstFile, 0)



# while firstFile.find_all('link'):
#     i = i + 1
#     print("Level ", i)
#     if i == 6:
#         break
#     for link in firstFile.find_all('link'):
#         print("New link")
#         filename = link.get("href").split('/')[-1]
#         path = path + "/" + filename
#         os.makedirs(path)
#         f = open(path + "/" + filename + ".xml", "w+")
#         f.write(BeautifulSoup(requests.get(link.get('href')).text, features="html.parser").prettify())
#         f.close()

# # print("Writing")
# f = open(sys.argv[1].split("/")[-1] + ".xml", "w+")
# f.write(soup.prettify())
# f.close()
# print("Done")