# wallstreetbots
Scraper on r/wallstreetbets, looking for mentioned stocks 

## About

My uncle asked if this is possible, so I did a small thing

## Disclaimer

**EDUCATIONAL USE ONLY** - This is basically just me practicing python and bs4.

## Usage

```shell
python scraper.py
```

**Options**: Edit the following constants near the top of `scraper.py`

* `PAGE` - number of items to retrieve per http request (prob shouldn't go over 100)
* `PAGE_COUNT` - number of pages (i.e. requests) to iterate through (akin to pressing the "next" button)

## Stonk matching

`allisted.txt` defines stonk symbols to search for (commal delimited). Any text in a title that matches one of these will be accounted for. Edit to add/remove

### Rate-limiting

`friendlybot.py` defines a class that honors `retry-after` headers on 429's, and sleeps to space out requests made close together.

GET DEM STONKS
