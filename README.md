# GEO Engine Runner — proceso reusable

Convierte cualquier sitio en **fuente citada por motores de IA** (ChatGPT/Perplexity/Gemini/Google AI Overviews/Claude). No optimiza para ranking SERP: optimiza para *knowledge retrieval*.

**Validado en producción:** `alterego.lat/recursos` (12 hubs, 2026-05-31). Caso anterior: biohackslabs.com (Shopify).

---

## Los 3 componentes

| Archivo | Qué hace |
|---|---|
| `geo_workflow.js` | Workflow parametrizado. Fases 1-4: entity map → query expansion → clustering → N artículos + social. Devuelve JSON estructurado. |
| `render.py` | Renderiza el JSON al HTML con el tema del sitio destino. JSON-LD `@graph` consolidado por página. Config-driven. |
| `deploy.py` | Deploy file-digest a Netlify + IndexNow. Config-driven con excludes. |

`configs/<sitio>.json` = config de render+deploy. `configs/<sitio>.args.json` = args del workflow (brand + categorías).

---

## Cómo correrlo en un sitio nuevo (4 pasos)

### 1. Armar la config y los args
Copiar `configs/alterego.json` → `configs/<sitio>.json` y editar: `domain`, `brand`, `site_dir`, `theme` (colores del sitio), `nav`, `cta`, `author`/`org` (con `@id` que matchee el del home para consolidar la entidad), `endcta`, y `_deploy.netlify_site_id`.

Copiar `configs/cursos-vraven.args.json` → `configs/<sitio>.args.json` y editar `brand_block` (posicionamiento + servicios + audiencia + **regla de honestidad**) y `categories` (4-8 áreas donde la marca quiere ser citada).

### 2. Correr el workflow
```
Workflow({ scriptPath: "/Users/hv/geo_engine_runner/geo_workflow.js",
           args: <contenido de configs/<sitio>.args.json> })
```
Guardar el `result` que devuelve (la parte `result` del output del task) en `<workdir>/result.json`.
~20 agents, ~950K tokens, ~8 min, ~US$7.

### 3. Renderizar
```
python3 render.py configs/<sitio>.json <workdir>/result.json
```
Genera `<site_dir>/<section_dir>/<slug>.html` (×N) + el índice + `sitemap_fragment.xml` + `llms_block.txt`.

### 4. Integrar + deploy
- Agregar link a la sección (`/recursos`) en el nav del home.
- Mergear `sitemap_fragment.xml` en el `sitemap.xml` del sitio.
- Crear/actualizar `llms.txt` en la raíz (usar `llms_block.txt`).
- Crear el key file de IndexNow en la raíz: `<key>.txt` con el contenido = la key. Poner `indexnow_key` + `result_json` en `_deploy` de la config.
- `python3 deploy.py configs/<sitio>.json`
- (manual) GSC: submit sitemap. (manual) Reddit: nunca bot.

---

## Decisiones de diseño (por qué así)

- **Los agents devuelven JSON, no HTML.** El render usa un template fijo del sitio → consistencia total. (En el caso Shopify, dejar que cada agent generara HTML produjo CSS disparejo y artículos condensados por límite de tool-call.)
- **JSON-LD `@graph` consolidado**, autor/publisher por `@id` que matchea el `#hernan`/`#org` del home. Los motores construyen UNA entidad para el autor en todo el sitio = E-E-A-T real. (Fix sobre la v1 de alterego, donde cada artículo declaraba un `Person` suelto sin `@id` → entidad fragmentada.)
- **Short-answer destacado arriba** = target #1 de extracción AI. Tabla en el fold + FAQ con FAQPage schema = formatos que los motores citan.
- **Regla de honestidad dura inyectada en cada agente.** Cero clientes/métricas/casos inventados. Lo que te hace citable y no sospechoso. NO negociable, sobre todo en YMYL.
- **Comparativos + how-tos primero** (≥50% P1). Son los que más rápido generan citación.

## Checklist de mejoras a verificar por sitio (lecciones acumuladas)
- [ ] `og_image` existe y está en el Article schema (no solo en el meta tag).
- [ ] `author.@id` y `org.@id` matchean EXACTO los `@id` del home (si el home tiene `@graph`).
- [ ] `sameAs` del autor: SOLO URLs verificables (LinkedIn/X reales). No inventar.
- [ ] hreflang si el sitio es bilingüe y hay versión EN (pendiente alterego).
- [ ] Los `.md`/internos siguen dando 404 tras el deploy (verificar en sitios con manifest estricto, ej. cursos.vraven.app).
- [ ] Link a la sección desde el footer de todas las páginas, no solo el nav del home.

---

## Timeline de citación esperado (referencia)
- Semana 1-2: crawl, 0 citas.
- Semana 3-4: primeras citas Perplexity (long-tail).
- Semana 6-8: ChatGPT Search (comparativas).
- Semana 8-12: Google AI Overviews.
- 3-6 meses: citación consistente cross-engine.

Medición: test semanal de 5-9 queries × 4 engines → CITED / MENTIONED / NOT PRESENT.

---

*GEO Engine Runner v1.1 — Vraven, 2026-05-31. Próximo target: cursos.vraven.app.*
