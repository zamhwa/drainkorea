#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update sitemap.xml with new city-specific SEO pages
"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime

DOCS_FOLDER = "/sessions/elegant-loving-heisenberg/jesus/docs"
SITEMAP_PATH = os.path.join(DOCS_FOLDER, "sitemap.xml")
AREA_FOLDER = os.path.join(DOCS_FOLDER, "area")
DOMAIN = "https://drainkorea.com"
TODAY = "2026-04-11"

# City romanization mapping
CITIES = {
    "수원": "suwan",
    "용인": "yongin",
    "성남": "seongnam",
    "부천": "bucheon",
    "인천": "incheon",
    "안양": "anyang",
    "안산": "ansan",
    "고양": "goyang",
    "파주": "paju",
    "김포": "gimpo",
    "화성": "hwaseong",
    "의정부": "uijeongbu",
    "남양주": "namyangju",
    "하남": "hanam",
    "광명": "gwangmyeong",
}

# Keywords mapping
KEYWORDS = {
    "하수구막힘": "hasugumaghim",
    "변기막힘": "byeongimaghim",
    "싱크대막힘": "singkeudaemaghim",
}


def read_existing_sitemap():
    """Read existing sitemap and preserve non-area URLs"""
    try:
        tree = ET.parse(SITEMAP_PATH)
        root = tree.getroot()
        return root
    except FileNotFoundError:
        # Create new root if file doesn't exist
        return ET.Element("urlset")


def create_url_element(loc, lastmod=TODAY, changefreq="weekly", priority="0.8"):
    """Create a URL element for sitemap"""
    url = ET.Element("url")

    loc_elem = ET.SubElement(url, "loc")
    loc_elem.text = loc

    if lastmod:
        lastmod_elem = ET.SubElement(url, "lastmod")
        lastmod_elem.text = lastmod

    if changefreq:
        freq_elem = ET.SubElement(url, "changefreq")
        freq_elem.text = changefreq

    if priority:
        priority_elem = ET.SubElement(url, "priority")
        priority_elem.text = priority

    return url


def main():
    # Read existing sitemap
    root = read_existing_sitemap()

    # Set namespace
    if root.tag == "urlset":
        ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
        root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    # Get all existing URLs
    existing_urls = set()
    for url_elem in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None:
            existing_urls.add(loc.text)

    # Also check without namespace
    for url_elem in root.findall("url"):
        loc = url_elem.find("loc")
        if loc is not None and loc.text:
            existing_urls.add(loc.text)

    new_urls_added = 0

    # Add new area pages
    for city_korean, city_roman in CITIES.items():
        for keyword_korean, keyword_roman in KEYWORDS.items():
            url_str = f"{DOMAIN}/area/{city_roman}-{keyword_roman}/"

            if url_str not in existing_urls:
                url_elem = create_url_element(url_str, TODAY, "weekly", "0.8")
                root.append(url_elem)
                existing_urls.add(url_str)
                new_urls_added += 1

    # Write updated sitemap
    tree = ET.ElementTree(root)
    tree.write(SITEMAP_PATH, encoding="utf-8", xml_declaration=True)

    print(f"✅ Sitemap updated successfully!")
    print(f"📝 New URLs added: {new_urls_added}")
    print(f"📊 Total URLs in sitemap: {len(existing_urls)}")
    print(f"📁 Sitemap location: {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
