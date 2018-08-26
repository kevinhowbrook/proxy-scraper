# Multithreaded scraper using proxies.

_This is a simple starting point for a basic(ish) webscraper using Python, Pipenv, BeautifulSoup, Pool, and Proxybroker_

> Scrape responsibly, see https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/#easiest-way-to-find-if-a-site-doesnt-want-data-to-be-scraped

### Running
First run `pipenv isntall` and `pipenv shell` to start the environment.

`python main.py` will start the scraping.

### Proxies
Proxies are generated via `proxies = gen_proxies`. This will populate a text file with a list of I.P addresses to use.

### Pool
Pool is set to 10: `with Pool(10) as p:` which means 10 requests. This can be increased or decreased. But be nice and don't actually DoS a site. :heart: