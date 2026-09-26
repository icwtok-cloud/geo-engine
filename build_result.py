#!/usr/bin/env python3
import json
from build_hubs import hubs
from articles_content import ARTICLES

articles = []
for h in hubs:
    a = ARTICLES.get(h["slug"])
    if not a:
        continue
    art = dict(a)
    art["slug"] = h["slug"]
    art["title"] = h["title"]
    art["_hub"] = h
    articles.append(art)

result = {
    "entity": {"primary": {"name": "Propomi", "domain": "propomi.lat", "description": "Portal inmobiliario LATAM"}, "services": [], "related": [], "adjacent": [], "relationships": []},
    "hubs": hubs,
    "articles": articles,
    "query_count": 0,
    "categories": ["guias de zona"],
}

with open("propomi_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"{len(articles)}/{len(hubs)} articulos listos:", ", ".join(a["slug"] for a in articles))
