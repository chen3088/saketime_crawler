# saketime_crawler

This repository contains simple crawlers for the Japanese sake ranking site "Saketime". The data for all regions is already bundled in `saketime_all_regions.csv`.

## Crawling brand details

To fetch information from each brand's detail page, run the helper
function defined in `brand_detail_crawler.py`:

```python
from brand_detail_crawler import crawl_brands_from_csv

crawl_brands_from_csv()
```

The function reads the URLs from `saketime_all_regions.csv`, crawls the
pages and saves a new file `saketime_brand_details.csv` with the parsed
information.
