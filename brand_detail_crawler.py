import csv
import time
import random
from typing import Dict, List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup


def crawl_brand_detail(url: str) -> Optional[Dict[str, str]]:
    """Crawl sake brand detail page and return parsed information.

    Parameters
    ----------
    url : str
        Detail page URL.

    Returns
    -------
    Optional[Dict[str, str]]
        Parsed brand information or None if request fails.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    title_tag = soup.find("meta", property="og:title")
    desc_tag = soup.find("meta", property="og:description")

    brand_name = title_tag["content"].strip() if title_tag else ""
    description = desc_tag["content"].strip() if desc_tag else ""

    prefecture = ""
    brewery = ""

    info_table = soup.select_one("table")
    if info_table:
        for tr in info_table.select("tr"):
            th = tr.select_one("th")
            td = tr.select_one("td")
            if not th or not td:
                continue
            key = th.text.strip()
            val = td.text.strip()
            if "地域" in key or "都道府県" in key:
                prefecture = val
            elif "蔵元" in key or "酒造" in key:
                brewery = val

    return {
        "brand_name": brand_name,
        "prefecture": prefecture,
        "brewery": brewery,
        "description": description,
    }


def crawl_brands_from_csv(csv_path: str = "saketime_all_regions.csv", output_csv: str = "saketime_brand_details.csv") -> None:
    """Crawl brand detail pages listed in ``csv_path`` and save to ``output_csv``.

    Parameters
    ----------
    csv_path : str
        Path to ``saketime_all_regions.csv`` that contains URLs under the ``詳細頁面連結`` column.
    output_csv : str
        Destination path of the crawled data.
    """
    df = pd.read_csv(csv_path)

    results: List[Dict[str, str]] = []
    for _, row in df.iterrows():
        url = row.get("詳細頁面連結")
        if not isinstance(url, str) or not url:
            continue
        info = crawl_brand_detail(url)
        if info:
            info["URL"] = url
            results.append(info)
        time.sleep(random.uniform(1.5, 3.0))

    if results:
        pd.DataFrame(results).to_csv(output_csv, index=False, encoding="utf-8-sig")

