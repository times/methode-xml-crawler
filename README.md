# Methode XML parser

This parser reads the methode XML given as an argument from an edition on the hub, crawls the tree as far as the depth set in the config, and outputs to `output` in the form `edition/book/section/slot/article/component`

Components in this case are related articles, images, interactive components etc.

It is important not to run a high depth or you may end up finding related articles that are related to one another, and cause an infinite loop. The program will stop at about 30 levels because of the file length (on MacOS).

## Running

To run the program use Python 3.7 or higher.

`pip install` from requirements.txt

Then run `python3 app.py <methode URL>`
