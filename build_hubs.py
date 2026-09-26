#!/usr/bin/env python3
import json, unicodedata, re

GEO_TARGETS = {
    "Argentina": ["Buenos Aires", "Córdoba", "Mendoza", "Rosario", "Salta", "La Plata"],
    "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Querétaro", "Tijuana", "Zapopan"],
}

def slugify(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

hubs = []
for country, cities in GEO_TARGETS.items():
    for city in cities:
        slug = slugify(f"{city}-{country}")
        hubs.append({
            "slug": slug,
            "title": f"Vivir en {city}: guía de zona y mercado inmobiliario",
            "h1": f"Guía de zona: {city}",
            "primary_query_es": f"como es vivir en {city}",
            "primary_query_en": f"what is it like living in {city}",
            "intent": "long-tail",
            "content_angle": f"guía de zona de {city}: mercado inmobiliario, vida de barrio y turismo conectable",
            "priority": "P1",
            "country": country,
            "city": city,
            "zone": "",
        })

if __name__ == "__main__":
    print(json.dumps(hubs, ensure_ascii=False, indent=2))
