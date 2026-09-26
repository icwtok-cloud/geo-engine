#!/usr/bin/env python3
"""Trae datos verificados de atracciones turisticas via la API de Wikipedia
(REST summary endpoint) para no inventar imagenes/nombres. Genera JSON con:
title, extract, image (thumb.wikimedia.org, verificado con la propia API),
wiki_url, maps_url (Google Maps search, siempre valido sin necesitar
place_id/coordenadas exactas)."""
import json, sys, urllib.request, urllib.parse

UA = "PropomiBot/1.0 (contact: hola@propomi.lat; guias de zona propomi.lat)"

# slug -> lista de titulos de pagina en es.wikipedia.org (nombre real, tal
# cual aparece en Wikipedia) para cada ciudad.
CITY_ATTRACTIONS = {
    "buenos-aires-argentina": ["Cementerio de la Recoleta", "Museo de Arte Latinoamericano de Buenos Aires", "Bosques de Palermo", "Caminito"],
    "cordoba-argentina": ["Manzana Jesuítica de Córdoba", "Patio Olmos", "Parque Sarmiento (Córdoba)", "Catedral de Córdoba (Argentina)"],
    "mendoza-argentina": ["Parque General San Martín (Mendoza)", "Plaza Independencia (Mendoza)", "Aconcagua"],
    "rosario-argentina": ["Monumento Nacional a la Bandera", "Parque de la Independencia (Rosario)", "Museo de Arte Contemporáneo de Rosario", "Isla de los Inventos"],
    "salta-argentina": ["Cerro San Bernardo (Salta)", "Catedral Basílica de Salta", "Tren a las Nubes", "Museo de Arqueología de Alta Montaña", "Quebrada de Humahuaca", "Cabildo de Salta"],
    "la-plata-argentina": ["Catedral de La Plata", "Museo de La Plata", "Plaza Moreno"],
    "ciudad-de-mexico-mexico": ["Bosque de Chapultepec", "Museo Nacional de Antropología (México)", "Palacio de Bellas Artes", "Templo Mayor", "Zócalo de la Ciudad de México"],
    "guadalajara-mexico": ["Catedral de Guadalajara", "Instituto Cultural Cabañas", "Teatro Degollado", "Mercado San Juan de Dios", "Templo Expiatorio del Santísimo Sacramento (Guadalajara)"],
    "monterrey-mexico": ["Parque Fundidora", "Cerro de la Silla", "Macroplaza", "Museo de Historia Mexicana"],
    "puebla-mexico": ["Catedral de Puebla", "Gran Pirámide de Cholula", "Museo Amparo", "Africam Safari"],
    "queretaro-mexico": ["Acueducto de Querétaro", "Jardín Zenea", "Templo de Santa Rosa de Viterbo"],
    "tijuana-mexico": ["Centro Cultural Tijuana", "Avenida Revolución (Tijuana)", "Playas de Tijuana", "Mercado Hidalgo (Tijuana)"],
    "zapopan-mexico": ["Basílica de Nuestra Señora de Zapopan", "Bosque Los Colomos", "Museo de Arte de Zapopan", "Andares (Zapopan)", "Estadio Akron"],
}

def fetch_summary(title, retries=5):
    import time
    url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(3 + attempt * 2)
                continue
            print(f"  WARN: {title} -> {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  WARN: {title} -> {e}", file=sys.stderr)
            return None
    return None

def maps_url(name, city):
    q = f"{name} {city}"
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)

def main():
    out = {}
    try:
        out = json.load(open("attractions.json", encoding="utf-8"))
    except FileNotFoundError:
        pass
    only = set(sys.argv[1:]) or None
    for slug, titles in CITY_ATTRACTIONS.items():
        if only and slug not in only:
            continue
        city = slug.split("-")[0].title()
        items = []
        for t in titles:
            import time; time.sleep(1.2)
            d = fetch_summary(t)
            if not d or not d.get("thumbnail", {}).get("source"):
                print(f"  SKIP (sin imagen o 404): {t}", file=sys.stderr)
                continue
            thumb = d["thumbnail"]["source"].split("?")[0]
            items.append({
                "name": d.get("title") or t,
                "extract": (d.get("extract") or "").strip(),
                "image": thumb,
                "wiki_url": f"https://es.wikipedia.org/wiki/{urllib.parse.quote(t.replace(' ', '_'))}",
                "maps_url": maps_url(d.get("title") or t, ""),
            })
            print(f"  OK: {t} -> {thumb}")
        out[slug] = items
    json.dump(out, open("attractions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\nTotal por ciudad:", {k: len(v) for k, v in out.items()})

if __name__ == "__main__":
    main()
