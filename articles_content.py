# -*- coding: utf-8 -*-
"""Contenido de los 13 artículos de guía de zona, escrito directamente
(sin el tool Workflow/agent del engine original, no disponible en esta
sesión). Formato: dict por slug, con los campos de ARTICLE_SCHEMA menos
slug/title/_hub (los agrega build_result.py al ensamblar)."""

ARTICLES = {}

ARTICLES["buenos-aires-argentina"] = {
    "meta_description": "Guía de zona de Buenos Aires: cómo es el mercado inmobiliario por barrio, vida de barrio real y qué conocer antes de mudarte o invertir en la ciudad.",
    "short_answer": "Buenos Aires concentra la mayor oferta inmobiliaria de Argentina, con barrios que van de torres modernas (Puerto Madero, Belgrano) a edificios de principios del siglo XX reciclados (Palermo, Recoleta, Caballito), y una vida de barrio muy caminable gracias al subte y al Metrobus.",
    "medium_answer": "La Ciudad Autónoma de Buenos Aires funciona como un mosaico de barrios con identidad propia, cada uno con su propio ritmo de rotación inmobiliaria: zonas como Palermo y Belgrano tienen alta demanda de departamentos de 1-2 ambientes por la cercanía a oficinas y vida nocturna, mientras que Caballito y Almagro atraen más a familias por el metro cuadrado más accesible y los colegios. Recoleta mantiene el perfil más tradicional, con edificios de categoría y proximidad a embajadas y museos. Moverse sin auto es perfectamente viable en casi toda la ciudad gracias al subte (6 líneas) y una red extensa de colectivos.",
    "bullets": [
        "El subte cubre los barrios de mayor demanda (Palermo, Recoleta, Caballito, Almagro, Once) — buena parte de la vida cotidiana no requiere auto.",
        "Puerto Madero es la zona de torres más nuevas de la ciudad, con el metro cuadrado más alto y vista al río.",
        "Palermo se divide en sub-zonas con personalidad propia: Palermo Soho (más bohemio/gastronómico), Palermo Hollywood (vida nocturna) y Palermo Chico (más residencial/tradicional).",
        "Caballito es uno de los barrios con mejor relación espacio/precio de la ciudad, con buena conexión de subte (línea A) y mucha oferta de colegios.",
        "Recoleta y Barrio Norte concentran el perfil más clásico: edificios de categoría, cercanía a museos (Bellas Artes, MALBA) y embajadas.",
        "Villa Crespo y Chacarita ganaron demanda en los últimos años como alternativa más accesible cerca de Palermo.",
        "Las ferias de barrio (Mataderos los domingos, la Feria de San Telmo) siguen siendo parte real de la vida social de esas zonas.",
    ],
    "sections": [
        {"h2": "Cómo se mueve el mercado inmobiliario por barrio",
         "body_html": "<p>Buenos Aires no tiene un único mercado inmobiliario: cada barrio se mueve distinto según quién lo busca. Palermo y Belgrano concentran la demanda de perfil profesional joven, con alta rotación de alquileres de 1-2 ambientes. Caballito y Almagro atraen más a familias que buscan más metros por el mismo presupuesto, sin resignar conexión de subte. Puerto Madero es un mercado aparte, orientado a torres nuevas con amenities. Recoleta mantiene una demanda más estable, con perfil de comprador que prioriza la categoría del edificio por sobre la modernidad.</p><p>Para quien busca invertir o mudarse, la variable que más pesa suele ser la cercanía a una estación de subte o a un corredor de colectivos troncal — eso explica por qué corredores como Av. Santa Fe, Av. Cabildo o Av. Rivadavia sostienen demanda constante independientemente del ciclo económico.</p>"},
        {"h2": "Vida de barrio: qué esperar día a día",
         "body_html": "<p>La vida de barrio porteña gira en torno al comercio de cercanía: kioscos, verdulerías y cafés a la vuelta de la esquina en casi cualquier zona residencial. Palermo y Villa Crespo tienen la escena gastronómica más activa de la ciudad, con una oferta que va del bodegón tradicional a propuestas de autor. Caballito y Almagro conservan un perfil más de barrio clásico, con plazas grandes (Parque Rivadavia, Parque Centenario) que funcionan como punto de encuentro de fin de semana.</p><p>La seguridad percibida varía bastante entre cuadras de un mismo barrio, más que entre barrios enteros — es habitual que quien busca mudarse recorra la cuadra específica de día y de noche antes de decidir, más que guiarse solo por el nombre del barrio.</p><ul><li>Transporte: subte + Metrobus cubren los corredores de mayor demanda.</li><li>Comercio de cercanía: fuerte en casi toda la ciudad, con variaciones de horario según el barrio.</li><li>Espacios verdes: Bosques de Palermo, Parque Centenario, Parque Rivadavia, Costanera Sur.</li></ul>"},
        {"h2": "Qué conocer si venís de otra ciudad o país",
         "body_html": "<p>Buenos Aires se recorre mucho a pie y en subte, algo distinto a ciudades de Latinoamérica más dependientes del auto. El clima templado permite usar espacios al aire libre casi todo el año, y el circuito cultural (teatros sobre Av. Corrientes, museos en Recoleta y Palermo) es parte cotidiana de la vida porteña, no solo un atractivo turístico.</p><p>Antes de decidir zona, vale la pena recorrer distintos barrios en distintos horarios: el perfil de una cuadra de Palermo a la mañana (oficinistas, cafés) es muy distinto al de la misma cuadra un viernes de noche.</p>"},
        {"h2": "Turismo y puntos de interés que conectan con la vida de barrio",
         "body_html": "<p>El Cementerio de la Recoleta y el MALBA son puntos de referencia real del barrio, no solo atracciones turísticas — muchos vecinos los cruzan a diario. Los Bosques de Palermo (con el Rosedal) funcionan como pulmón verde de toda la zona norte de la ciudad. San Telmo, con su feria de anticuarios de los domingos, mantiene un perfil más bohemio y es un buen termómetro de cómo se ve la reconversión de barrios históricos.</p><p>Estos puntos no son solo para visitar: son parte de por qué esas zonas sostienen demanda inmobiliaria a largo plazo — la cercanía a un espacio verde grande o a un circuito cultural activo pesa tanto como la cercanía al subte a la hora de elegir dónde vivir.</p>"},
    ],
    "comparison_table": {
        "caption": "Perfil de barrios de Buenos Aires según qué busca el comprador/inquilino",
        "headers": ["Barrio", "Perfil típico", "Fortaleza principal"],
        "rows": [
            ["Palermo", "Profesional joven, sin hijos", "Vida nocturna y gastronomía"],
            ["Belgrano", "Familias, perfil más tradicional", "Colegios y espacios verdes"],
            ["Recoleta", "Comprador de categoría", "Museos, embajadas, edificios clásicos"],
            ["Caballito", "Familias, primera compra", "Relación espacio/precio, subte línea A"],
            ["Puerto Madero", "Perfil corporativo/inversión", "Torres nuevas, vista al río"],
            ["Villa Crespo", "Joven, busca alternativa a Palermo", "Precio más accesible, buena conexión"],
            ["Almagro", "Familias y estudiantes", "Centralidad, buen transporte"],
            ["San Telmo", "Perfil bohemio/inversión turística", "Identidad histórica, feria dominical"],
        ],
    },
    "faqs": [
        {"q": "¿Cuál es el barrio más buscado de Buenos Aires para alquilar?", "a": "Palermo suele liderar la demanda de alquiler por su cercanía a oficinas, vida nocturna y variedad de departamentos chicos, aunque Belgrano y Caballito también concentran mucha búsqueda, especialmente de perfil familiar."},
        {"q": "¿Se puede vivir en Buenos Aires sin auto?", "a": "Sí, es lo más habitual en la mayoría de los barrios céntricos y de zona norte gracias al subte y al Metrobus — el auto se vuelve más necesario en barrios de zona sur o GBA con menor cobertura de transporte."},
        {"q": "¿Qué diferencia hay entre Palermo Soho y Palermo Hollywood?", "a": "Palermo Soho tiene un perfil más gastronómico y de diseño/moda, mientras que Palermo Hollywood concentra más bares y vida nocturna — ambos dentro del mismo barrio grande de Palermo."},
        {"q": "¿Recoleta es una buena zona para invertir?", "a": "Recoleta mantiene demanda estable por su perfil de categoría, museos y cercanía a zonas corporativas, aunque el metro cuadrado suele estar entre los más altos de la ciudad."},
        {"q": "¿Cómo es la vida de barrio en Caballito?", "a": "Caballito conserva un perfil de barrio clásico porteño, con plazas grandes, comercio de cercanía activo y buena oferta de colegios — es de los barrios preferidos por familias que buscan más espacio sin salir de la ciudad."},
        {"q": "¿Puerto Madero es solo para perfil corporativo?", "a": "Es el foco principal de la zona, pero también atrae a inversores por la modernidad de los edificios y la vista al río, aunque tiene menos vida de barrio tradicional que el resto de la ciudad."},
        {"q": "¿Qué zonas verdes tiene Buenos Aires cerca del centro?", "a": "Los Bosques de Palermo (con el Rosedal), Parque Centenario y Parque Rivadavia son los espacios verdes más grandes y usados dentro de la ciudad."},
        {"q": "¿Vale la pena recorrer un barrio antes de mudarse?", "a": "Sí, la percepción de seguridad y el perfil de vecindario pueden variar bastante entre cuadras de un mismo barrio, así que recorrer de día y de noche antes de decidir es una práctica habitual."},
    ],
    "definitions": [
        {"term": "Subte", "definition": "Red de metro de Buenos Aires, con 6 líneas que cubren buena parte de los barrios de mayor demanda."},
        {"term": "Metrobus", "definition": "Sistema de carriles exclusivos para colectivos que agiliza corredores troncales como Av. Cabildo o Av. Juan B. Justo."},
        {"term": "Ambiente (amb.)", "definition": "Unidad de medida típica argentina para describir departamentos: '2 ambientes' equivale aproximadamente a 1 dormitorio + living."},
        {"term": "GBA", "definition": "Gran Buenos Aires, el conurbano que rodea a la Ciudad Autónoma de Buenos Aires."},
        {"term": "CABA", "definition": "Ciudad Autónoma de Buenos Aires, el distrito propiamente dicho (distinto del Gran Buenos Aires/GBA)."},
    ],
    "social": {
        "linkedin_es": "Buenos Aires no tiene un mercado inmobiliario, tiene 48 (uno por barrio). Palermo no se mueve igual que Caballito, y Recoleta no se mueve igual que Puerto Madero. Armamos una guía de zona con el perfil real de cada barrio: quién vive ahí, qué tan bien se mueve sin auto, y qué mirar antes de elegir. La subimos a Propomi para que sirva como referencia antes de buscar propiedad, no solo como contenido turístico. Si estás por mudarte o invertir en la ciudad, puede ahorrarte semanas de recorrer barrios al pedo.",
        "twitter_es": "Buenos Aires tiene 48 barrios y ningún mercado inmobiliario único.\n\nPalermo ≠ Caballito ≠ Recoleta ≠ Puerto Madero.\n\nArmamos una guía real de zona (no solo turística) para saber qué esperar antes de mudarte.",
        "twitter_en": "Buenos Aires has 48 neighborhoods and no single real estate market.\n\nPalermo ≠ Caballito ≠ Recoleta ≠ Puerto Madero.\n\nWe put together a real zone guide (not just tourism) for what to expect before moving.",
    },
}
