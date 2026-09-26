export const meta = {
  name: 'geo-engine',
  description: 'GEO Engine reusable: entity map -> query expansion -> intent clustering -> N article hubs + social, optimizados para citacion en motores IA. Parametrizado via args.',
  phases: [
    { title: 'Entity Map' },
    { title: 'Query Expansion' },
    { title: 'Clustering' },
    { title: 'Articles' },
  ],
}

// ===== args esperados (pasar como JSON en la invocacion Workflow) =====
// {
//   brand_block: string,        // bloque de contexto de marca (posicionamiento, servicios, stack, audiencia, reglas)
//   categories: string[],       // 4-8 categorias de conocimiento donde la marca quiere ser citada
//   hub_count?: number,         // cantidad de hubs (default 12)
//   lang_primary?: string,      // "es" | "en" (default "es")
//   persona?: string,           // quien "escribe" los articulos (ej "Hernan Vega, operador...")
//   honesty_rule?: string,      // regla de honestidad dura especifica del sitio
//   cta_line?: string,          // CTA sutil al pie de cada articulo (ej "agenda un diagnostico en alterego.lat/agendar")
// }
let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { log('args llego como string no-JSON') } }
const BRAND = A.brand_block || ''
const CATS = A.categories || []
const HUB_COUNT = A.hub_count || 12
const LANG = A.lang_primary || 'es'
const PERSONA = A.persona || 'un operador experto de la marca'
const HONESTY = A.honesty_rule || 'No inventar clientes, metricas ni casos de exito de terceros. Mostrar capacidad y metodo.'
const CTA = A.cta_line || 'invita sutilmente a contactar a la marca al final'
const LANG_NOTE = LANG === 'es' ? 'espanol (LATAM neutro), ~70% ES y ~30% EN en queries' : 'English primary, ~30% Spanish in queries'
// Modo zona (geo_targets): {country: [city,...], ...}. Si viene, los hubs son
// 1 por ciudad (deterministico, sin query-expansion/clustering por LLM) — para
// sitios que necesitan cobertura garantizada de zonas puntuales (ej. hot-zones
// de una campaña de ads) en vez de topicos de conocimiento genericos.
const GEO_TARGETS = A.geo_targets || null

function slugify(s) {
  return String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().trim().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'')
}

if (!BRAND || (CATS.length === 0 && !GEO_TARGETS)) {
  log('ERROR: faltan args.brand_block y/o args.categories (o args.geo_targets). Abortando.')
  return { error: 'missing args', got: Object.keys(A) }
}

phase('Entity Map')
const ENTITY_SCHEMA = { type:'object', additionalProperties:false, required:['primary','services','related','adjacent','relationships'], properties:{
  primary:{type:'object',additionalProperties:false,required:['name','domain','description'],properties:{name:{type:'string'},domain:{type:'string'},description:{type:'string'}}},
  services:{type:'array',items:{type:'object',additionalProperties:false,required:['name','description'],properties:{name:{type:'string'},description:{type:'string'}}}},
  related:{type:'array',items:{type:'string'}}, adjacent:{type:'array',items:{type:'string'}}, relationships:{type:'array',items:{type:'string'}} } }
const entity = await agent(
  `Sos un estratega de Generative Engine Optimization. Construi el knowledge graph (entity map) para esta marca.\n${BRAND}\n\nDevolve: primary entity (la marca), service/product entities, related entities (conceptos directamente conectados), adjacent entities (mercado expandido) y semantic relationships (frases que conectan entidades). Objetivo: que los motores IA citen a la marca como fuente para queries de su nicho.`,
  { phase:'Entity Map', schema:ENTITY_SCHEMA, label:'entity-map' })

const HUBS_SCHEMA = { type:'object', additionalProperties:false, required:['hubs'], properties:{ hubs:{type:'array',items:{type:'object',additionalProperties:false,
  required:['slug','title','h1','primary_query_es','primary_query_en','intent','content_angle','priority'], properties:{
  slug:{type:'string'},title:{type:'string'},h1:{type:'string'},primary_query_es:{type:'string'},primary_query_en:{type:'string'},
  intent:{type:'string',enum:['commercial','comparative','high-traffic','authority','long-tail']}, content_angle:{type:'string'}, priority:{type:'string',enum:['P1','P2','P3']},
  country:{type:'string'}, city:{type:'string'}, zone:{type:'string'} }}} } }

let hubs, allQueries = []
if (GEO_TARGETS) {
  // Modo zona: hubs deterministicos, 1 por ciudad. Sin LLM en esta fase —
  // ahorra el costo/tiempo de Query Expansion + Clustering cuando la lista
  // de zonas ya viene dada (ej. las mismas hot-zones de una campaña de ads).
  phase('Query Expansion'); log('modo zona: sin query expansion, geo_targets ya define la cobertura')
  phase('Clustering')
  hubs = []
  for (const [country, cities] of Object.entries(GEO_TARGETS)) {
    for (const city of cities) {
      const slug = slugify(`${city}-${country}`)
      hubs.push({
        slug, title: `Vivir en ${city}: guía de zona y mercado inmobiliario`, h1: `Guía de zona: ${city}`,
        primary_query_es: `como es vivir en ${city}`, primary_query_en: `what is it like living in ${city}`,
        intent: 'long-tail', content_angle: `guía de zona (mercado inmobiliario + vida de barrio + turismo) de ${city}, con datos reales del catálogo de la marca`,
        priority: 'P1', country, city, zone: '',
      })
    }
  }
  log(`${hubs.length} hubs de zona definidos (modo geo_targets)`)
} else {
  phase('Query Expansion')
  const QUERY_SCHEMA = { type:'object', additionalProperties:false, required:['queries'], properties:{ queries:{type:'array',items:{type:'object',additionalProperties:false,required:['q','type','lang'],properties:{
    q:{type:'string'}, type:{type:'string',enum:['informational','comparative','commercial','conversational','objection']}, lang:{type:'string',enum:['es','en']} }}} } }
  const queryBatches = await parallel(CATS.map((cat,i)=>()=>
    agent(`Generador de queries para GEO. Para la categoria: "${cat}".\n${BRAND}\n\nGenera 40-60 queries REALES que el cliente ideal de esta marca escribiria en ChatGPT/Perplexity/Gemini/Google AI. Mezcla los 5 tipos: informational (que es / como funciona / como hacer X), comparative (X vs Y), commercial (a quien contratar/comprar, cuanto cuesta, mejor opcion), conversational (me conviene X?, puedo combinar X con Y?), objection (esto funciona?, vale la pena?). Idioma: ${LANG_NOTE}. Queries naturales y especificas, no keywords sueltas.`,
      { phase:'Query Expansion', schema:QUERY_SCHEMA, label:`queries:${i+1}` })
  )).then(r=>r.filter(Boolean))
  allQueries = queryBatches.flatMap(b=>b.queries)
  log(`${allQueries.length} queries across ${CATS.length} categorias`)

  phase('Clustering')
  const clustering = await agent(
    `Sos un arquitecto de contenido GEO. Te paso ${allQueries.length} queries reales para esta marca.\n${BRAND}\n\nQUERIES (muestra):\n${JSON.stringify(allQueries.slice(0,220).map(q=>q.q))}\n\nClusteriza en EXACTAMENTE ${HUB_COUNT} content hubs (paginas). Priorizá comparativos y how-tos (los que mas rapido generan citacion). Cada hub: slug (kebab-case sin acentos, en ${LANG}), title (<=60 chars), h1, primary_query_es, primary_query_en, intent, content_angle (el angulo unico que solo ESTA marca puede dar, no generico), priority (P1=quick win comercial/comparativo, P2=high-traffic, P3=authority). Al menos ${Math.ceil(HUB_COUNT/2)} P1. Cubri todas las categorias. Slugs unicos y URL-safe.`,
    { phase:'Clustering', schema:HUBS_SCHEMA, label:'clustering' })
  hubs = clustering.hubs.slice(0, HUB_COUNT)
  log(`${hubs.length} hubs definidos`)
}

phase('Articles')
const ARTICLE_SCHEMA = { type:'object', additionalProperties:false,
  required:['slug','title','meta_description','short_answer','medium_answer','bullets','sections','comparison_table','faqs','definitions','social'], properties:{
  slug:{type:'string'}, title:{type:'string'}, meta_description:{type:'string'}, short_answer:{type:'string'}, medium_answer:{type:'string'},
  bullets:{type:'array',items:{type:'string'}},
  sections:{type:'array',items:{type:'object',additionalProperties:false,required:['h2','body_html'],properties:{h2:{type:'string'},body_html:{type:'string'}}}},
  comparison_table:{type:'object',additionalProperties:false,required:['caption','headers','rows'],properties:{caption:{type:'string'},headers:{type:'array',items:{type:'string'}},rows:{type:'array',items:{type:'array',items:{type:'string'}}}}},
  faqs:{type:'array',items:{type:'object',additionalProperties:false,required:['q','a'],properties:{q:{type:'string'},a:{type:'string'}}}},
  definitions:{type:'array',items:{type:'object',additionalProperties:false,required:['term','definition'],properties:{term:{type:'string'},definition:{type:'string'}}}},
  social:{type:'object',additionalProperties:false,required:['linkedin_es','twitter_es','twitter_en'],properties:{linkedin_es:{type:'string'},twitter_es:{type:'string'},twitter_en:{type:'string'}}} } }
const zoneNote = (h) => GEO_TARGETS ? `\n\nESTO ES UN HUB DE ZONA (ciudad: ${h.city}, pais: ${h.country}). Ademas de las secciones pedidas, la mezcla de angulos tiene que cubrir: (a) mercado inmobiliario real de esa zona (tipos de propiedad, rango de precios orientativo, rotacion), (b) vida de barrio (servicios, transporte, quien vive ahi), (c) 2-3 actividades turisticas o puntos de interes genuinamente conocidos de esa ciudad que conecten con el momento de mudarse/visitar/invertir (sin inventar direcciones ni negocios puntuales no verificables). Mezclalos en las mismas secciones, no los separes en "turismo" vs "inmobiliaria" como si fueran temas distintos — el lector tiene que sentir que es UNA guia de la zona.` : ''
const articles = await parallel(hubs.map(h=>()=>
  agent(`Sos ${PERSONA}. Escribi el contenido COMPLETO de un articulo de knowledge-hub para GEO, tan util y especifico que un motor IA lo cite como fuente autoritativa.\n${BRAND}\n\nHUB:\n- slug: ${h.slug}\n- title: ${h.title}\n- h1: ${h.h1}\n- query objetivo ES: ${h.primary_query_es}\n- query objetivo EN: ${h.primary_query_en}\n- angulo: ${h.content_angle}\n- intent: ${h.intent}${zoneNote(h)}\n\nIDIOMA: ${LANG === 'es' ? 'espanol (LATAM neutro)' : 'English'}. Produci:\n1. short_answer: 1-2 oraciones que responden la query de forma extractable (target #1 de extraccion AI). Densas, factuales.\n2. medium_answer: 1 parrafo (4-6 oraciones) con detalle de mecanismo/metodo.\n3. bullets: 5-8 bullets especificos.\n4. sections: 4-6 secciones, cada una h2 + body_html (150-300 palabras en HTML simple: <p>, <ul><li>, <strong>; SIN clases CSS, SIN <h2> dentro del body). Profundidad operativa real, ejemplos concretos, pasos accionables.\n5. comparison_table: tabla relevante a la query (caption, 2-4 headers, 6-12 rows con valores concretos).\n6. faqs: 8-10 preguntas reales, respuestas 2-4 oraciones.\n7. definitions: 5-8 terminos clave.\n8. social: linkedin_es (120-180 palabras, hook+valor+CTA suave), twitter_es (thread compacto con saltos de linea), twitter_en (idem EN).\n\nHONESTIDAD DURA: ${HONESTY}. CTA: ${CTA}. El slug del output debe ser exactamente "${h.slug}".`,
    { phase:'Articles', schema:ARTICLE_SCHEMA, label:`article:${h.slug}` }).then(a=>({...a,_hub:h}))
)).then(r=>r.filter(Boolean))
log(`${articles.length}/${hubs.length} articulos generados`)

return { entity, hubs, articles, query_count: allQueries.length, categories: CATS }
