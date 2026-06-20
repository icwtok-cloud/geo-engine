#!/usr/bin/env python3
"""GEO Engine — renderer config-driven. Convierte el result.json de un run del
workflow (articulos JSON estructurado) en HTML con el tema del sitio destino.

Uso: python3 render.py <config.json> <result.json>

config.json define dominio, tema, nav, autor/org (para JSON-LD @graph consolidado),
y textos de la seccion. Reusable para cualquier sitio (alterego.lat, cursos.vraven.app, ...).

Genera en <site_dir>:
  <section_dir>/<slug>.html   (1 por hub, JSON-LD @graph: WebPage+Article+Person+Org+Breadcrumb + FAQPage)
  <section_dir>.html          (indice de la seccion)
Y en el dir del runner: sitemap_fragment.xml + llms_block.txt
"""
import json, sys, html, pathlib

def esc(s): return html.escape(str(s), quote=True)

def build_css(t):
    return f'''*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{t["bg"]};color:{t["text"]};font-family:{t.get("font",'-apple-system,"Helvetica Neue",Helvetica,Arial,sans-serif')};line-height:1.65}}
a{{color:{t["accent"]};text-decoration:none}}a:hover{{text-decoration:underline}}
.topbar{{display:flex;justify-content:space-between;align-items:center;padding:14px 26px;border-bottom:1px solid {t["border"]};background:radial-gradient(800px 200px at 50% -50%,{t.get("glow","#1d1840")} 0,{t["bg"]} 70%);position:sticky;top:0;z-index:10;gap:10px}}
.logo svg{{height:22px;display:block}}.logo b{{font-weight:900;font-size:19px;color:{t["text"]};letter-spacing:1px}}
.controls{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end}}
.controls a{{font-size:12.5px;font-weight:700;color:{t["muted"]}}}
.controls .cta{{background:{t["accent"]};color:{t["bg"]};padding:8px 15px;border-radius:8px;white-space:nowrap}}
.controls .cta:hover{{background:#fff;text-decoration:none}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px}}
.crumb{{font-size:12px;color:{t["muted"]};padding:22px 0 0}}.crumb a{{color:{t["muted"]}}}
.kicker{{display:inline-block;font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:{t["accent2"]};font-weight:800;margin:26px 0 14px;padding:6px 13px;border:1px solid {t["border"]};border-radius:99px}}
h1{{font-size:clamp(30px,4.6vw,44px);line-height:1.12;font-weight:900;color:#fff;letter-spacing:-.5px;margin-bottom:18px}}
.answer{{background:linear-gradient(135deg,{t["accent"]}1a,{t["accent2"]}14);border:1px solid {t["accent"]};border-left:4px solid {t["accent"]};border-radius:12px;padding:20px 24px;margin:6px 0 26px;font-size:17px;color:#fff;font-weight:600}}
.lede{{font-size:16px;color:{t["textbody"]};margin-bottom:24px}}
.bullets{{background:{t["card"]};border:1px solid {t["border"]};border-radius:12px;padding:20px 24px 20px 40px;margin:0 0 30px}}
.bullets li{{margin:7px 0;color:{t["textbody"]};font-size:15px}}
h2{{font-size:24px;font-weight:900;color:#fff;margin:36px 0 14px;letter-spacing:-.3px}}
h3{{font-size:18px;color:{t["accent"]};margin:20px 0 8px}}
p{{margin:0 0 14px;color:{t["textbody"]};font-size:15.5px}}
ul,ol{{margin:0 0 16px 22px}}li{{margin:6px 0;color:{t["textbody"]};font-size:15.5px}}
strong{{color:#fff}}
table{{width:100%;border-collapse:collapse;margin:18px 0 28px;font-size:14px;background:{t["card"]};border:1px solid {t["border"]};border-radius:10px;overflow:hidden}}
caption{{caption-side:top;text-align:left;color:{t["muted"]};font-size:13px;margin-bottom:8px;font-style:italic}}
th{{background:{t["accent2"]}26;color:#fff;text-align:left;padding:11px 14px;font-weight:800;border-bottom:1px solid {t["border"]}}}
td{{padding:10px 14px;border-bottom:1px solid {t["border"]};color:{t["textbody"]};vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.faq{{margin:14px 0 30px}}
.faq details{{border:1px solid {t["border"]};border-radius:10px;margin-bottom:10px;background:{t["card"]}}}
.faq summary{{padding:15px 18px;font-weight:700;color:#fff;cursor:pointer;font-size:15.5px;list-style:none}}
.faq summary::-webkit-details-marker{{display:none}}
.faq summary::after{{content:"+";float:right;color:{t["accent"]};font-weight:900}}
.faq details[open] summary::after{{content:"–"}}
.faq details p{{padding:0 18px 16px;margin:0;color:{t["textbody"]};font-size:14.5px}}
.defs{{display:grid;gap:12px;margin:14px 0 30px}}
.def{{border-left:3px solid {t["accent2"]};padding:4px 0 4px 16px}}
.def b{{color:{t["accent"]};font-size:15px}}.def span{{display:block;color:{t["textbody"]};font-size:14.5px;margin-top:3px}}
.related{{background:{t["card"]};border:1px solid {t["border"]};border-radius:12px;padding:20px 24px;margin:10px 0 26px}}
.related h3{{color:#fff;margin:0 0 12px}}.related a{{display:block;padding:6px 0;font-size:14.5px;border-bottom:1px solid {t["border"]}}}.related a:last-child{{border:none}}
.endcta{{background:linear-gradient(135deg,{t["accent"]}1f,{t["accent2"]}1f);border:1px solid {t["accent"]};border-radius:14px;padding:28px 26px;margin:34px 0;text-align:center}}
.endcta h3{{color:{t["accent"]};font-size:21px;margin-bottom:8px;border:none}}
.endcta p{{color:{t["text"]};margin-bottom:16px}}
.endcta .btn{{background:{t["accent"]};color:{t["bg"]};padding:12px 24px;border-radius:9px;font-weight:800;display:inline-block}}
.endcta .btn:hover{{background:#fff;text-decoration:none}}
.byline{{font-size:13px;color:{t["muted"]};margin:24px 0 6px;border-top:1px solid {t["border"]};padding-top:18px}}.byline b{{color:{t["accent"]}}}
footer{{padding:34px 26px;border-top:1px solid {t["border"]};text-align:center;font-size:12px;color:{t["muted"]};margin-top:30px}}footer a{{color:{t["accent"]};font-weight:700}}
@media(max-width:600px){{.controls a:not(.cta){{display:none}}.topbar{{padding:11px 14px}}.logo svg{{height:18px}}}}'''

def logo_html(cfg):
    if cfg.get("logo_svg"):
        return f'<a class="logo" href="/" aria-label="{esc(cfg["brand"])}">{cfg["logo_svg"]}</a>'
    return f'<a class="logo" href="/" aria-label="{esc(cfg["brand"])}"><b>{esc(cfg["brand"])}</b></a>'

def nav_html(cfg):
    links = "".join(f'<a href="{esc(l["href"])}">{esc(l["label"])}</a>' for l in cfg.get("nav", []))
    cta = cfg["cta"]
    return f'''<div class="topbar">
  {logo_html(cfg)}
  <div class="controls">{links}<a class="cta" href="{esc(cta["href"])}">{esc(cta["label"])}</a></div>
</div>'''

def footer_html(cfg):
    if cfg.get("footer_html"): return cfg["footer_html"]
    fl = " · ".join(f'<a href="{esc(l["href"])}">{esc(l["label"])}</a>' for l in cfg.get("footer_links", cfg.get("nav", [])))
    return f'''<footer><p><b>{esc(cfg["brand"])}</b> — {esc(cfg.get("footer_tagline",""))} · <a href="/">{cfg["domain"].split("//")[1]}</a></p><p style="margin-top:6px">{fl}</p></footer>'''

def graph_ld(cfg, a, url, title):
    """JSON-LD @graph consolidado: Org + Person + WebPage + Article + Breadcrumb + FAQPage.
    author/publisher por @id => consolida la entidad en todo el sitio (clave para GEO/E-E-A-T)."""
    au, org = cfg["author"], cfg["org"]
    today = cfg.get("date", "2026-05-31")
    person = {"@type":"Person","@id":au["id"],"name":au["name"],"url":au["url"]}
    if au.get("jobTitle"): person["jobTitle"]=au["jobTitle"]
    if au.get("sameAs"): person["sameAs"]=au["sameAs"]
    person["worksFor"]={"@id":org["id"]}
    organ = {"@type":"Organization","@id":org["id"],"name":org["name"],"url":org["url"],"logo":org.get("logo")}
    if org.get("sameAs"): organ["sameAs"]=org["sameAs"]
    webpage = {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,
               "isPartOf":{"@id":cfg["domain"]+"/#website"},"inLanguage":cfg.get("lang","es"),
               "breadcrumb":{"@id":url+"#breadcrumb"},"primaryImageOfPage":cfg.get("og_image")}
    website = {"@type":"WebSite","@id":cfg["domain"]+"/#website","url":cfg["domain"]+"/","name":cfg["brand"],"publisher":{"@id":org["id"]}}
    article = {"@type":"Article","@id":url+"#article","headline":a["title"],"description":a["meta_description"],
               "datePublished":today,"dateModified":today,"author":{"@id":au["id"]},"publisher":{"@id":org["id"]},
               "image":cfg.get("og_image"),"mainEntityOfPage":{"@id":url+"#webpage"},"inLanguage":cfg.get("lang","es"),
               "isPartOf":{"@id":cfg["domain"]+"/#website"}}
    crumb = {"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":cfg["domain"]+"/"},
        {"@type":"ListItem","position":2,"name":cfg["section_name"],"item":cfg["domain"]+cfg["section_path"]},
        {"@type":"ListItem","position":3,"name":title,"item":url}]}
    faq = {"@type":"FAQPage","@id":url+"#faq","mainEntity":[
        {"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in a["faqs"]]}
    return {"@context":"https://schema.org","@graph":[website,organ,person,webpage,article,crumb,faq]}

def render_article(cfg, a, related):
    slug=a["slug"]; url=f'{cfg["domain"]}{cfg["section_path"]}/{slug}'; title=a["title"]
    secs="".join(f'<h2>{esc(s["h2"])}</h2>\n{s["body_html"]}\n' for s in a["sections"])
    bl="".join(f"<li>{esc(b)}</li>" for b in a["bullets"])
    t=a["comparison_table"]
    thead="".join(f"<th>{esc(h)}</th>" for h in t["headers"])
    trows="".join("<tr>"+"".join(f"<td>{esc(c)}</td>" for c in row)+"</tr>" for row in t["rows"])
    table=f'<table><caption>{esc(t["caption"])}</caption><thead><tr>{thead}</tr></thead><tbody>{trows}</tbody></table>'
    faqs="".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in a["faqs"])
    defs="".join(f'<div class="def"><b>{esc(d["term"])}</b><span>{esc(d["definition"])}</span></div>' for d in a["definitions"])
    rel="".join(f'<a href="{cfg["section_path"]}/{r["slug"]}">{esc(r["title"])}</a>' for r in related)
    ec=cfg["endcta"]; btn_href=ec["btn_href_tmpl"].format(slug=slug)
    h1=a.get("_hub",{}).get("h1", title)
    return f'''<!DOCTYPE html>
<html lang="{cfg.get("lang","es")}"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {esc(cfg["brand"])}</title>
<meta name="description" content="{esc(a["meta_description"])}">
<meta name="author" content="{esc(cfg["author"]["name"])}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(a["meta_description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{cfg.get("og_image","")}">
<meta property="og:site_name" content="{esc(cfg["brand"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico">
<script type="application/ld+json">{json.dumps(graph_ld(cfg,a,url,title), ensure_ascii=False)}</script>
<style>{build_css(cfg["theme"])}</style></head>
<body>
{nav_html(cfg)}
<div class="wrap">
  <div class="crumb"><a href="/">Inicio</a> › <a href="{cfg["section_path"]}">{esc(cfg["section_name"])}</a> › {esc(title)}</div>
  <span class="kicker">{esc(cfg.get("article_kicker","Recurso"))}</span>
  <h1>{esc(h1)}</h1>
  <div class="answer">{esc(a["short_answer"])}</div>
  <p class="lede">{esc(a["medium_answer"])}</p>
  <ul class="bullets">{bl}</ul>
  {secs}
  {table}
  <h2>Preguntas frecuentes</h2>
  <div class="faq">{faqs}</div>
  <h2>Definiciones clave</h2>
  <div class="defs">{defs}</div>
  <div class="related"><h3>Recursos relacionados</h3>{rel}</div>
  <div class="endcta"><h3>{esc(ec["title"])}</h3><p>{esc(ec["body"])}</p><a class="btn" href="{esc(btn_href)}">{esc(ec["btn_label"])}</a></div>
  <p class="byline">Por <b>{esc(cfg["author"]["name"])}</b> · {esc(cfg.get("author",{}).get("jobTitle",""))} · {cfg.get("date","2026-05-31")}</p>
</div>
{footer_html(cfg)}
</body></html>'''

def render_index(cfg, articles):
    cards=""
    for a in articles:
        cards+=f'''<article class="post"><span class="tag">{esc(a.get("_hub",{}).get("intent","guia"))}</span>
        <h2><a href="{cfg["section_path"]}/{a["slug"]}">{esc(a.get("_hub",{}).get("h1",a["title"]))}</a></h2>
        <p>{esc(a["meta_description"])}</p></article>\n'''
    ld={"@context":"https://schema.org","@type":"CollectionPage","name":f'{cfg["section_name"]} · {cfg["brand"]}',
        "url":cfg["domain"]+cfg["section_path"],"inLanguage":cfg.get("lang","es"),"description":cfg["section_desc"]}
    t=cfg["theme"]
    return f'''<!DOCTYPE html>
<html lang="{cfg.get("lang","es")}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(cfg["section_title"])} · {esc(cfg["brand"])}</title>
<meta name="description" content="{esc(cfg["section_desc"])}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{cfg["domain"]+cfg["section_path"]}">
<meta property="og:title" content="{esc(cfg["section_title"])}"><meta property="og:url" content="{cfg["domain"]+cfg["section_path"]}">
<meta property="og:image" content="{cfg.get("og_image","")}">
<link rel="icon" href="/favicon.ico">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{build_css(t)}
.hero{{max-width:820px;margin:0 auto;padding:54px 24px 18px;text-align:center}}.hero h1{{margin-bottom:12px}}.hero p{{color:{t["textbody"]};max-width:600px;margin:0 auto;font-size:16px}}
.posts{{max-width:820px;margin:24px auto 50px;padding:0 24px;display:grid;gap:16px}}
.post{{background:{t["card"]};border:1px solid {t["border"]};border-radius:12px;padding:22px 24px;transition:.16s}}
.post:hover{{border-color:{t["accent"]};transform:translateY(-2px)}}
.post .tag{{display:inline-block;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:{t["accent2"]};font-weight:800;margin-bottom:8px;border:1px solid {t["accent2"]}66;padding:3px 9px;border-radius:99px}}
.post h2{{font-size:20px;margin:0 0 8px}}.post h2 a{{color:#fff}}.post h2 a:hover{{color:{t["accent"]};text-decoration:none}}
.post p{{color:{t["textbody"]};font-size:14px;margin:0}}</style></head>
<body>
{nav_html(cfg)}
<section class="hero"><span class="kicker">{esc(cfg.get("section_kicker","Knowledge base"))}</span>
<h1>{esc(cfg["section_title"])}</h1><p>{esc(cfg["section_desc"])}</p></section>
<div class="posts">
{cards}</div>
{footer_html(cfg)}
</body></html>'''

def main():
    cfg=json.load(open(sys.argv[1])); data=json.load(open(sys.argv[2]))
    articles=data["articles"]
    site=pathlib.Path(cfg["site_dir"]); out=site/cfg["section_dir"]; out.mkdir(parents=True,exist_ok=True)
    for a in articles:
        same=[x for x in articles if x is not a and x.get("_hub",{}).get("intent")==a.get("_hub",{}).get("intent")]
        related=(same+[x for x in articles if x is not a and x not in same])[:3]
        (out/f'{a["slug"]}.html').write_text(render_article(cfg,a,related),encoding="utf-8")
    (site/f'{cfg["section_dir"]}.html').write_text(render_index(cfg,articles),encoding="utf-8")
    runner=pathlib.Path(__file__).parent
    base=cfg["domain"]+cfg["section_path"]; today=cfg.get("date","2026-05-31")
    frag=f'  <url>\n    <loc>{base}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    frag+="".join(f'  <url>\n    <loc>{base}/{a["slug"]}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n' for a in articles)
    (runner/"sitemap_fragment.xml").write_text(frag,encoding="utf-8")
    llms=[f'- [{a["title"]}]({base}/{a["slug"]}): {a["meta_description"]}' for a in articles]
    (runner/"llms_block.txt").write_text("\n".join(llms),encoding="utf-8")
    print(f'OK: {len(articles)} articulos + indice en {out}')
    print("slugs:", ", ".join(a["slug"] for a in articles))

if __name__=="__main__": main()
