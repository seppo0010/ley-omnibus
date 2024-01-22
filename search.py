import re
import json
import sys
import os

def c(x):
    return x.replace('quáter', 'quater')

def rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'Deróg(?:a|ue)se (?:la Ley|el Decreto Ley) N° ([0-9\.]+).*', x)
    if m is None: return None
    ley, = m.groups()
    ley = ley.replace('.', '')
    with open(f'leyes/ley{ley}.txt') as fp:
        old = fp.read()

    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": old,
        "textoModificado": "" if num != 61 else 'Apruébase la Ley de Defensa de la Competencia que se adjunta como ANEXO III (IF-2023-153144565-APN-SSAL#SLYT)',
    }

def rich_data_derogase_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:Deróguese|Der[óo]gan?se) (?:los artículos|el artículo) ([\d\s(?: bis),° y]+)(?:.*?)(de la [lL]ey|del Decreto-Ley|del Decreto de Necesidad y Urgencia|del Código Civil y Comercial)(?:.*?)\s*[Nº° ]*([\d\.\/]+).*?', x)
    if m is None: return None
    arts, lod, ley = m.groups()
    arts = [art.strip() for art in arts.replace('\n', ' ').replace('°', '').replace('y', '').replace(',', '').split(' ')]
    arts = [art for art in arts if art != '']
    arts = ','.join(arts).replace(',bis', ' bis').split(',')
    ley = ley.replace('.', '').replace('/', '-')
    f = f'leyes/ley{ley}.txt'
    if lod == 'del Decreto de Necesidad y Urgencia':
        f = f'leyes/dnu{ley}.txt'
    with open(f) as fp:
        old = fp.read()
    art_old = [re.search(r'\nART(?:[ÍI]CULO)?\.?\s*' + art + r'((?:.|\n)*?)\nART', old, re.I).groups()[0] for art in arts]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": '\n'.join(art_old),
        "textoModificado": "",
    }

def rich_data_sustituyese_articulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    if num == 550:
        x = x.replace('de Educación nacional.', 'de Educación nacional, por el siguiente:')
    m = re.match(r'(?:.*?)(?:Sustit[uú]y[ae]se|Modifícase)(?:, a partir del 1° de abril de 2024,)? el artículo (\d+)[°º]?( (?:bis|ter|quater|quáter|quinquies|sixties|septies))?,? (?:(?:de )?(?:la )?[lL]ey|del Decreto[- ]Ley)(?:.*?) N?[°º ]*([\d\.\/]+)(?:.*?)(?: por el siguiente(?: texto)?|, el que quedará redactado como sigue|, el cual quedará redactado de la siguiente manera):(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, bis, ley, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/ley{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + 'º?' + c('' if bis is None else bis) + r'(?:.|\n)*?)\nART', c(old), re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_new,
    }

def rich_data_sustituyese_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustit[uú]yen?se(?:, con efectos a partir del período fiscal 2023 inclusive,)? los artículos ([\d\s,y]+)(?: del Título [IVXCLD]+) (?:(?:de )?la Ley|del Decreto-Ley)(?:.*?) N[°º ]*([\d\.\/]+)(?:.*?) por los siguientes(?: texto)?:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    arts_str, ley, art_new = m.groups()
    arts = [art for art in re.sub(r'\s+', ' ', arts_str.replace(',', '').replace('y', '')).split(' ')]
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/ley{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = [re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + 'º?' r'(?:.|\n)*?)\nART', c(old), re.I).groups()[0] for art in arts]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": '\n'.join(art_old),
        "textoModificado": art_new,
    }

def rich_data_sustituyese_articulo_cpn(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el artículo (\d+)[°º]? del Código Penal(?: de la Nación)?,? por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    with open(f'leyes/cpn.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_new,
    }

def rich_data_sustituyese_articulo_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el artículo (\d+)[°º]? del Código Civil y Comercial(?:.*?) por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    with open(f'leyes/ccyc.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_new,
    }

def rich_data_sustituyese_parrafo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    x = x.replace('Ley de Impuesto al Valor Agregado', 'Decreto 280/97')
    m = re.match(r'(?:.*?)Sustitúyese,?(?: en)? el(?: (primer|segundo|tercer|cuarto))? párrafo(?: (primero|segundo|tercero|cuarto))? del artículo (\d+)[°º]?(?: (:bis|ter|quater|quáter|quinquies|sixties|septies))? de la (Ley|Decreto)(?:.*?) (?:N[°º] )?([\d\.\/]+)(?:.*?) por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL|re.I)
    if m is None: return None
    par, par2, art, bis, lod, ley, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/{"ley" if lod.lower() == "ley" else "decreto"}{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + 'º?\s*' + c('' if bis is None else bis) + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    paragraphs = re.split(r'\n+', art_old)
    paragraphs[{
        'primer': 0,
        'primero': 0,
        'segundo': 1,
        'tercer': 2,
        'tercero': 2,
        'cuarto': 3,
    }[par if par is not None else par2]] = art_new
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": '\n'.join(paragraphs),
    }

def rich_data_sustituyese_articulo_dnu(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el artículo (\d+)[°º]? del Decreto de Necesidad y Urgencia N° ([0-9/]+),? por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, dnu, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    dnu = dnu.replace('.', '').replace('/', '-')
    with open(f'leyes/dnu{dnu}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_new,
    }

def rich_data_derogase_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Derógase el inciso ([a-z0-9]+)\)? del artículo (\d+)[°º]? del Código Civil y Comercial(?:.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    inc, art = m.groups()

    with open('leyes/ccyc.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": re.sub(r'\b' + inc + r'[\)\.].*', '', art_old),
    }

def rich_data_derogase_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Der[oó]gase el inciso ([a-z0-9]+)\)? del artículo (\d+)[°º]? (del Decreto|de la Ley) N[°º] ([\d\.\/]+)(?:.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    inc, art, lod, ley = m.groups()

    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/{"ley" if lod == "de la Ley" else "decreto"}{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": re.sub(r'\b' + inc + r'[\)\.].*', '', art_old),
    }

def rich_data_derogase_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Deroguese los incisos ([,\)a-z0-9\s]+) del [Aa]rt[ií]culo (\d+)[°º]? (del Decreto|de la Ley) N[°º] ([\d\.\/]+)(?:.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    inc, art, lod, ley = m.groups()
    incs = re.sub(r'\s', ' ', inc.replace(' y ', ',')).replace(' ', '').split(',')

    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/{"ley" if lod == "de la Ley" else "decreto"}{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    art_new = art_old
    for inc in incs:
        art_new = re.sub(r'\n' + re.escape(inc) + r'.*', '', art_new)
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_new,
    }

def rich_data_sustituyese_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el inciso ([a-z0-9]+)\)?[°º]? del artículo (\d+)[°º]? de la Ley (?:.*?)N[°º] ([\d\.]+)(?:.*),? por el siguiente(?: texto)?:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    inc, art, ley, inc_new = m.groups()
    inc_new = inc_new.replace('“', '')
    inc_new = inc_new.replace('”', '')
    inc_new = inc_new.strip()

    ley = ley.replace('.', '')
    with open(f'leyes/ley{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'º?(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": re.sub(inc + r'º?[\)\.].*', inc_new, art_old),
    }
def rich_data_incorporase_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Incorpóranse como incisos (?:.*?)(?:del )?artículo (\d+)[°º]? (?:(?:de )?(?:la )?[lL]ey|del Decreto[- ]Ley)(?:.*?) N?[°º ]*([\d\.\/]+)(?:.*?) que estarán redactados de la siguiente manera:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, ley, inc_new = m.groups()
    inc_new = inc_new.replace('“', '')
    inc_new = inc_new.replace('”', '')


    ley = ley.replace('.', '')
    with open(f'leyes/ley{ley}.txt') as fp:
        old = fp.read() + '\nART'
    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_old + f' \n{inc_new}',
    }

def rich_data_incorporase_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Incorpórase como inciso (?:[a-z])\)? (?:del )?artículo (\d+)[°º]? del Código Civil y Comercial (?:.*?)el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, inc_new = m.groups()
    inc_new = inc_new.replace('“', '')
    inc_new = inc_new.replace('”', '')

    with open(f'leyes/ccyc.txt') as fp:
        old = fp.read() + '\nART'
    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": art_old + f' \n{inc_new}',
    }

def rich_data_sustituyese_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el inciso ([a-z])\)? (?:del )?artículo (\d+)[°º]? del Código Civil y Comercial (?:.*?)por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    inc, art, inc_new = m.groups()
    inc_new = inc_new.replace('“', '')
    inc_new = inc_new.replace('”', '')
    inc_new = inc_new.strip()

    with open(f'leyes/ccyc.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"  TÍTULO {titulo} - {titulo_titulo}\r\n  CAP\u00cdTULO {capitulo} - {capitulo_titulo}",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": art_old,
        "textoModificado": re.sub(inc + r'[\)\.].*', inc_new, art_old),
    }

def rich_data_sustituyese_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    return None

def rich_data_switch(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    opt = rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo_dnu(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo_cpn(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_parrafo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_incorporase_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_incorporase_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    if (x.startswith('Sustit') or x.startswith('Modif')) and not x.startswith('Sustitúyese la denominación'):
        print({"num": num, "x": x})
    return {
        "fechaDescarga": "29/12/2023, 08:50:32",
        "json_original": {
            "tipoNorma": "",
            "nroNorma": "",
            "anioNorma": 0,
            "nombreNorma": "",
            "leyenda": "  ",
            "fechaPromulgacion": "",
            "fechaPublicacion": "",
            "vistos": "  ",
            "tituloArticulo": f"",
            "nombreArticulo": "",
            "textoArticulo": "",
            "notasArticulo": "",
            "firmantes": ""
        },
        "numeroArticulo": str(num),
        "seccionArticulo": titulo,
        "capituloArticulo": capitulo,
        "textoArticulo": '',
        "notasArticulo": "",
        "textoOriginal": "",
        "textoModificado": x,
    }
def rich_data(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    data = rich_data_switch(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    data['textoOriginal'] = data['textoOriginal'].replace('ARTICULO', 'ARTÍCULO').lstrip('-. ')
    data['textoModificado'] = data['textoModificado'].replace('ARTICULO', 'ARTÍCULO').lstrip('-. ')
    return data

fp = open('omnibus')
data = fp.read()
data = re.sub(r'\n{2,}', '[enter]', data)
data = data.replace('\n', ' ')
data = data.replace('[enter]', '\n')

ESTA = int(sys.argv[1]) if len(sys.argv) == 2 else None
if ESTA is None:
    indice = open('src/content/meta/indice.yaml', 'w')

for num, x in enumerate(re.split('[^“]ART[ÍI]CULO', data)):
    if num == 0: continue
    if ESTA is not None and num != ESTA: continue
    titulo, titulo_titulo = 'I', ''
    capitulo, capitulo_titulo = 'I', ''
    num = int(num)
    x = x.strip()
    x = x.strip('°°º\u00b0')
    x = x.lstrip('.- 0123456789\u00b0[]*')
    #if ESTA is not None:
    #    print(rich_data(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo))
    #    break

    json_file = open(f'src/content/luc/LUC_articulo_{num}.json', "w")
    data = rich_data(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    json_file.write(json.dumps(data, indent=4))
    json_file.close()
    if ESTA is None:
        texto = data["textoModificado"]
        if len(texto) == 0:
            texto = data["textoOriginal"]
        texto = re.sub(r'^ART([íi]cULO|\.)?\s+\d+[º°]?\s*(bis|ter|qu[aá]ter|quinquies|sixties|septies|octies)?', '', texto, flags=re.I)
        texto = texto.lstrip('.-º—°').strip()
        texto = re.sub(r'^Incorpór[ea]se.*?[““]', '', texto, flags=re.MULTILINE | re.I | re.DOTALL)
        texto = re.sub(r'^ART([íi]cULO|\.)?\s+\d+[º°]?\s*(bis|ter|qu[aá]ter|quinquies|sixties|septies|octies)?', '', texto, flags=re.I)
        texto = texto.lstrip('.-º—°').strip()
        texto = {}.get(num, texto)
        desc = '' # re.split(r'[:\.\(]', texto)[0].replace("\n", " ").replace('"', '\\"')
        indice.write(f'''
- NRO_SECCION: "I"
  DESC_SECCION: ""
  NRO_CAPITULO: "I"
  DESC_CAPITULO: ""
  NRO_ARTICULO: {num}
  DESC_ARTICULO: "{desc}"
  RAW: {json.dumps(x)}
             '''.strip())
        indice.write('\n')