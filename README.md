# Matricula Online Scraper
[Matricula Online](https://data.matricula-online.eu/) is an online resource that contains various records used for genealogical research. This program can download any collection of scanned images from the site while preserving relevant information about the document and individual scans.
## Installation
**Make sure you are using Python >=3.6**

To Install Files:
```bash
git clone https://github.com/1fge/matricula-online-scraper
```
To Install Required Modules:
```bash
pip install -r requirements.txt
```

## Usage
After installing the dependencies, the scraper can be used directly from the command line.

To Download a Single Archive:
```bash
python main.py -o ./images -u https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001
```
To Download a List of Archive URLs from a File:
```bash
python main.py -o ./images -t ./urls.txt
```
If you run into any problems, feel free to create an issue. Furthermore, your contribution is encouraged, so feel free to make a pull request if you think something can be improved. Enjoy!
