# Matricula Online Scraper
[Matricula Online](https://data.matricula-online.eu/) is an online resource that contains various records used for genealogical research. This program can download any collection of scanned images from the site while preserving relevant information about the document and individual scans.
## Installation
**Make sure you are using Python >=3.6**

To Install Files:
```sh
git clone https://github.com/1fge/matricula-online-scraper
```
To Install Required Modules:
```sh
pip install -r requirements.txt
```

If you have a newer version of Python (e.g. Python-3.10),
you might need to get the latest and greatest versions of the various dependencies,
in which case you should run this instead:

```sh
pip install -r requirements-dev.txt
```


## Usage
After installing the dependencies, the scraper can be used directly from the command line.

To Download a Single Archive:
```sh
python matricula-online-scraper -o ./images -u https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001
```

On some systems (e.g. Linux, or macOS) you might also be able to run simply with:
```sh
./matricula-online-scraper -o ./images -u https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001
```



To Download a List of Archive URLs from a File:
```sh
python matricula-online-scraper -o ./images -t ./urls.txt
```
To Download a Range of Pages from an Archive:
```sh
python matricula-online-scraper -o ./images -r 10 -u https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001
```

### Directory hierarchy
Normally, the scraper will create a single directory for each parish+book, e.g. in the above example it will create a directory `images/militaerkirchenbuecher_0001/`.

Sometimes (when downloading many books from different parishes), it might be more desirable to have a single directory for all books of a given parish. Use the `--deep` flag to create directories like `images/militaerkirchenbuecher/0001/`:

```sh
python matricula-online-scraper --deep  -o ./images -r 10 -u https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001
```

### Directory names
Normally, the scraper will create a directory per collection, using the names found on the given webpage.
Sometimes this is can be a bit cryptic, as many collections use a simple numeric ID to identify them.
You can use the `--include-fullname` option to *add* a human readable string (taken from the webpage) that explains the content of the collection.

E.g. the collection found at https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001 will normally have a simple ID `0001`, but with `--include-fullname` this will become `0001__Aachen - Taufen` which probably makes more sense.

Note that extracting the names from the webpage is a bit brittle. You can use the `--simple-dirnames` to skip this step and just calculate the directory name from the URL itself
(so https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001 will become `militaerkirchenbuecher_0001` (using the last two components of the URL).

### Scraper behaviour
Use the `--continue` flag to skip already downloaded files.
This is useful if you are interrupted halfway through downloading a 500 pages collection...

## Issues
If you run into any problems, feel free to create an issue. Furthermore, your contribution is encouraged, so feel free to make a pull request if you think something can be improved. Enjoy!
