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
    m = re.match(r'(?:Deróguese|Der[óo]gan?se) (?:los artículos|el artículo) ([\d\s(?: bis),° y]+)(?:.*?)(de la [lL]ey|del Decreto-Ley|del Decreto de Necesidad y Urgencia|del Código Civil y Comercial)(?:.*?)\s*[No\.º° ]*([\d\.\/]+).*?', x)
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

def rich_data_derogase_titulo(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    derogado = None
    if declared_num == -1:
        with open('leyes/ley23905.txt') as fp:
            derogado = re.search(r'(TITULO VII\n.*?)TITULO VIII\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    elif declared_num == -1:
        with open('leyes/ley26571.txt') as fp:
            derogado = re.search(r'(TITULO II\n.*?)TITULO III\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    elif declared_num == -1:
        with open('leyes/ley23351.txt') as fp:
            derogado = re.search(r'(TITULO IV\n.*?)TITULO V\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    elif declared_num == -1:
        with open('leyes/ley23351.txt') as fp:
            derogado = re.search(r'(TITULO V\n.*?)TITULO VI\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    else:
        return None

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
        "textoOriginal": derogado,
        "textoModificado": "",
    }

def rich_data_sustituyese_articulo(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    x = x.replace('del Código Electoral Nacional, Ley 19.945, el que queda redactado de la siguiente manera:', 'de la Ley 19.945, por el siguiente texto:')
    m = re.match(r'(?:.*?)(?:Sustit[uú]y[ae]se|Modifícase)(?:, a partir del 1° de abril de 2024,)? el artículo (\d+)[°º]?( (?:bis|ter|quater|quáter|quinquies|sixties|septies|undecies))?,? ((?:de )?(?:la )?[lL]ey|del Decreto[- ]Ley|del Decreto)(?:.*?) N?[°º ]*([\d\.\/]+)(?:.*?)(?: por el siguiente(?: texto)?|, el que quedará redactados? como sigue|, el cual quedará redactado de la siguiente manera):(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, bis, lod, ley, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    ley = ley.replace('.', '').replace('/', '-')
    lod_str = 'decreto' if lod == 'del Decreto' else 'ley'
    with open(f'leyes/{lod_str}{ley}.txt') as fp:
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
    m = re.match(r'(?:.*?)Sustit[uú]yen?se(?:, con efectos a partir del período fiscal 2023 inclusive,)? los artículos ([\d\s,y]+)(?: del Título [IVXCLD]+)? (?:(?:de )?la Ley|del Decreto-Ley)(?:.*?) N[°º ]*([\d\.\/]+)(?:.*?)(?: por los siguientes(?: texto)?|por el siguiente):(.*)', x, re.MULTILINE|re.DOTALL)
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
    m = re.match(r'(?:.*?)Sustitúyese el artículo (\d+)[°º]? del Código Penal(?: de la Nación)?,? por el siguiente(?: texto)?:(.*)', x, re.MULTILINE|re.DOTALL)
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
    m = re.match(r'(?:.*?)Sustitúyese,?(?: en)? el(?: (primer|segundo|tercer|cuarto|quinto))? párrafo(?: (primero|segundo|tercero|cuarto))? del artículo (\d+)[°º]?(?: (:bis|ter|quater|quáter|quinquies|sixties|septies))? (?:de|por) la (Ley|Decreto)(?:.*?) (?:N[°º] )?([\d\.\/]+)(?:.*?) por el siguiente(?: texto)?:(.*)', x, re.MULTILINE|re.DOTALL|re.I)
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
    m = re.match(r'(?:.*?)(?:Incorpóranse|Incorpórase) como incisos? (?:.*?)(?:del )?artículo (\d+)[°º]?(?:.*?)(?:(?:de )?(?:la )?[lL]ey|del Decreto[- ]Ley)(?:.*?) N?[°º ]*([\d\.\/]+)(?:.*?)(?:, el siguiente| que estarán redactados de la siguiente manera):(.*)', x, re.MULTILINE|re.DOTALL)
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

def rich_data_sustituyese_incisos(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    if declared_num == 280:
        ley = 'ley26741'
        art = '3'
        incs = {
            'd': 'La maximización de las inversiones y de los recursos empleados para el logro del abastecimiento de hidrocarburos en el corto, mediano y largo plazo;',
            'g': 'La protección de los intereses de los consumidores relacionados con la calidad y disponibilidad de los derivados de hidrocarburos;',
            'h': 'La exportación de hidrocarburos para el mejoramiento de la balanza de pagos, garantizando la explotación racional de los recursos y la sustentabilidad de su explotación para el aprovechamiento de las generaciones futuras',
        }
    elif declared_num == 336:
        ley = 'ccyc'
        art = '1514'
        incs = {
            'a': 'proporcionar, a satisfacción del franquiciado, información relevante sobre la evolución del negocio, en el país o en el extranjero;',
            'b': 'comunicar al franquiciado el conjunto de conocimientos técnicos, aun cuando no estén patentados, derivados de la experiencia del franquiciante y considerados por las partes aptos para producir los efectos del sistema franquiciado;',
        }
    elif declared_num == 439:
        ley = 'ley24449'
        art = '40'
        incs = {
            'a': 'Que su conductor esté habilitado para conducir ese tipo de vehículo y que lleve consigo la licencia correspondiente; en el caso de los vehículos autodirigidos, que cuenten con un software de conducción autorizado previamente en el país.',
            'b': 'Que porte la cédula de identificación del mismo, la cual podrá ser exhibida en formato papel impreso o digital a través de dispositivos electrónicos.',
        }
    else:
        return None

    with open(f'leyes/{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    art_new = art_old
    for i, t in incs.items():
        art_new = re.sub('\n(' + i + r'[\)\. ]+).*', f'\\1{t}', art_new)
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

def rich_data_192(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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
        "textoOriginal": 'Artículo 18: Por el expendio de los tabacos para ser consumidos en hoja, despalillados, picados, en hebras, pulverizados (rapé), en cuerda, en tabletas y despuntes, el fabricante, importador y/o fraccionador pagará el veinticinco por ciento (25%) sobre la base imponible respectiva. No obstante lo establecido en el párrafo anterior, el impuesto que corresponda ingresar no podrá ser inferior a cuarenta pesos ($ 40) por cada 50 gramos o proporción equivalente. Ese importe se actualizará conforme a lo indicado en el cuarto párrafo del artículo 15, resultando también de aplicación lo previsto en el quinto párrafo del mismo artículo. Los elaboradores o fraccionadores de tabacos que utilicen en sus actividades productos gravados por este artículo podrán computar como pago a cuenta del impuesto que deban ingresar, el importe correspondiente al impuesto abonado o que se deba abonar por dichos productos con motivo de su expendio, en la forma que establezca la reglamentación.',
        "textoModificado": 'Artículo 18: Por el expendio de los tabacos para ser consumidos en hoja, despalillados, picados, en hebras, pulverizados (rapé), en cuerda, en tabletas y despuntes, el fabricante, importador y/o fraccionador pagará el veinticinco por ciento (25%) sobre la base imponible respectiva. No obstante lo establecido en el párrafo anterior, el impuesto que corresponda ingresar no podrá ser inferior a cuarenta pesos ($ 40) por cada 50 gramos o proporción equivalente. Este importe se actualizará conforme a lo indicado en el cuarto párrafo del artículo 16. Los elaboradores o fraccionadores de tabacos que utilicen en sus actividades productos gravados por este artículo podrán computar como pago a cuenta del impuesto que deban ingresar, el importe correspondiente al impuesto abonado o que se deba abonar por dichos productos con motivo de su expendio, en la forma que establezca la reglamentación.',
    }

def rich_data_163(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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
        "textoOriginal": 'ARTÍCULO ...- El transporte de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, fuera de los establecimientos y locales debidamente habilitados que se efectúe, sin importar su destino, sin el correspondiente respaldo documental de traslado o con documentación de traslado con irregularidades, será sancionado con una multa equivalente al importe que surja de la aplicación de lo dispuesto en el segundo, tercer y cuarto párrafo del artículo 15, en, proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco transportado por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo del traslado cuando se dé alguno de los siguientes supuestos:\n\na) La documentación de traslado sea apócrifa.\n\nb) Existan diferencias entre las cantidades de producto transportado y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo de la mercadería detectada y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el remitente del tabaco. En caso de desconocerse la procedencia del tabaco, se considerará responsable al destinatario (adquirente: comerciante, manufacturero, importador), al titular del tabaco, o a las empresas de transporte, en ese orden.\n\nIguales disposiciones resultarán aplicables cuando la mercadería transportada en las condiciones descriptas se trate de las comprendidas en los artículos 15, 16 y 18. En estos casos, el monto de la multa a la que se refiere el primer párrafo será equivalente al del impuesto que surgiría de aplicar las disposiciones de los referidos artículos, según corresponda, considerando el momento de la detección de la situación descripta.',
        "textoModificado": 'ARTÍCULO ...- El transporte de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, fuera de los establecimientos y locales debidamente habilitados que se efectúe, sin importar su destino, sin el correspondiente respaldo documental de traslado o con documentación de traslado con irregularidades, será sancionado con una multa equivalente al importe que resulte de aplicar la alícuota dispuesta en el primer párrafo del artículo 15 sobre el precio que surja del relevamiento al que se refiere el artículo sin número agregado a continuación del artículo 2°, en proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco transportado por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo del traslado cuando se dé alguno de los siguientes supuestos:\n\na) La documentación de traslado sea apócrifa.\n\nb) Existan diferencias entre las cantidades de producto transportado y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo de la mercadería detectada y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el remitente del tabaco. En caso de desconocerse la procedencia del tabaco, se considerará responsable al destinatario (adquirente: comerciante, manufacturero, importador), al titular del tabaco, o a las empresas de transporte, en ese orden.\n\nIguales disposiciones resultarán aplicables cuando la mercadería transportada en las condiciones descriptas se trate de las comprendidas en los artículos 15, 16 y 18. En estos casos, el monto de la multa a la que se refiere el primer párrafo será equivalente al del impuesto que surgiría de aplicar las disposiciones de los referidos artículos, según corresponda, considerando el momento de la detección de la situación descripta.',
    }

def rich_data_164(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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
        "textoOriginal": 'ARTÍCULO ...- El transporte de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, fuera de los establecimientos y locales debidamente habilitados que se efectúe, sin importar su destino, sin el correspondiente respaldo documental de traslado o con documentación de traslado con irregularidades, será sancionado con una multa equivalente al importe que surja de la aplicación de lo dispuesto en el segundo, tercer y cuarto párrafo del artículo 15, en, proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco transportado por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo del traslado cuando se dé alguno de los siguientes supuestos:\n\na) La documentación de traslado sea apócrifa.\n\nb) Existan diferencias entre las cantidades de producto transportado y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo de la mercadería detectada y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el remitente del tabaco. En caso de desconocerse la procedencia del tabaco, se considerará responsable al destinatario (adquirente: comerciante, manufacturero, importador), al titular del tabaco, o a las empresas de transporte, en ese orden.\n\nIguales disposiciones resultarán aplicables cuando la mercadería transportada en las condiciones descriptas se trate de las comprendidas en los artículos 15, 16 y 18. En estos casos, el monto de la multa a la que se refiere el primer párrafo será equivalente al del impuesto que surgiría de aplicar las disposiciones de los referidos artículos, según corresponda, considerando el momento de la detección de la situación descripta.',
        "textoModificado": 'ARTÍCULO ...- El transporte de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, fuera de los establecimientos y locales debidamente habilitados que se efectúe, sin importar su destino, sin el correspondiente respaldo documental de traslado o con documentación de traslado con irregularidades, será sancionado con una multa equivalente al importe que surja de la aplicación de lo dispuesto en el segundo, tercer y cuarto párrafo del artículo 15, en, proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco transportado por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo del traslado cuando se dé alguno de los siguientes supuestos:\n\na) La documentación de traslado sea apócrifa.\n\nb) Existan diferencias entre las cantidades de producto transportado y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo de la mercadería detectada y las que figuran en la documentación de traslado, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el remitente del tabaco. En caso de desconocerse la procedencia del tabaco, se considerará responsable al destinatario (adquirente: comerciante, manufacturero, importador), al titular del tabaco, o a las empresas de transporte, en ese orden.\n\nIguales disposiciones resultarán aplicables cuando la mercadería transportada en las condiciones descriptas se trate de las comprendidas en los artículos 15, 16 y 18. En estos casos, el monto de la multa a la que se refiere el primer párrafo será equivalente al del impuesto que surgiría de aplicar las disposiciones de los referidos artículos y del artículo agregado a continuación del artículo 2°, según corresponda, considerando el momento de la detección de la situación descripta.',
    }

def rich_data_165(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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
        "textoOriginal": 'ARTÍCULO ...- La existencia de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, sin importar su destino, sin el correspondiente respaldo documental o con documentación con irregularidades, será sancionada con una multa equivalente al importe que surja de la aplicación de lo, dispuesto en el segundo, tercer y cuarto párrafo del artículo 15, en proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco en existencia por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo cuando se de alguno de los siguientes supuestos:\n\na) La documentación sea apócrifa.\n\nb) Existan diferencias entre las cantidades de producto en existencia y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo, de la mercadería detectada y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el tenedor de las existencias de tabaco.',
        "textoModificado": 'ARTÍCULO ...- La existencia de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, sin importar su destino, sin el correspondiente respaldo documental o con documentación con irregularidades, será sancionada con una multa equivalente al importe que resulte de aplicar la alícuota dispuesta en el primer párrafo del artículo 15 sobre el precio que surja del relevamiento al que se refiere el artículo sin número agregado a continuación del artículo 2°, en proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco en existencia por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo cuando se de alguno de los siguientes supuestos:\n\na) La documentación sea apócrifa.\n\nb) Existan diferencias entre las cantidades de producto en existencia y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo, de la mercadería detectada y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el tenedor de las existencias de tabaco.',
    }

def rich_data_470(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    with open(f'leyes/ley26215.txt') as fp:
        old = fp.read() + '\nART'
    arts = [
        '16', '35', '43', '44 bis', '45', '47', '43 bis', '43 ter', '43 quáter', '43 quinquies', '43 sexies', '43 septies', '43 octies',
        '43 nonies', '44 ter', '44 quáter', '44 quinquies',
    ]
    art_old = [re.search(r'(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, flags=re.I | re.MULTILINE).groups()[0] for art in arts]
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
        "textoModificado": '',
    }

def rich_data_switch(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    if declared_num != num:
        raise Exception(f'num ({num}) != declared_num ({declared_num})\n{x}')
    if declared_num == 163:
        return rich_data_163(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if declared_num == 164:
        return rich_data_164(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if declared_num == 165:
        return rich_data_165(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    opt = rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_titulo(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
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
    opt = rich_data_sustituyese_incisos(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_incorporase_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_incorporase_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    if (x.startswith('Sustit') or x.startswith('Modif')) and not x.startswith('Sustitúyese la denominación') and not x.startswith('Sustitúyese el nombre de la sección'):
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
def rich_data(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    data = rich_data_switch(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    data['textoOriginal'] = data['textoOriginal'].replace('ARTICULO', 'ARTÍCULO').lstrip('-. ')
    data['textoModificado'] = data['textoModificado'].replace('ARTICULO', 'ARTÍCULO').lstrip('-. ')
    return data

fp = open('omnibus')
data = fp.read()
data = re.sub(r'\n{2,}', '[enter]', data)
data = data.replace('\n', ' ')
data = data.replace('[enter]', '\n')
capitulos = []
for capitulo, titulo, numart in re.findall('[^“]CAP[ÍI]TULO ([IXVL]+)(.*$)\n*ART[ÍI]CULO\s*(\d+)', data, re.MULTILINE):
    titulo = titulo.strip().replace('- ', '').replace('– ', '')
    capitulos.append((capitulo, titulo, int(numart)))

titulos = []
for titulo_num, titulo, numart in re.findall('[^“]T[ÍI]TULO ([IXVL]+)(.*$)(?:\n*CAP[IÍ]TULO.*?)?(?:\n*Sección.*?)?\n*ART[ÍI]CULO\s*(\d+)', data, re.MULTILINE):
    titulo = titulo.strip().replace('- ', '').replace('– ', '')
    titulos.append((titulo_num, titulo, int(numart)))

ESTA = int(sys.argv[1]) if len(sys.argv) == 2 else None
if ESTA is None:
    indice = open('src/content/meta/indice.yaml', 'w')

for num, x in enumerate(re.split('[^“]ART[ÍI]CULO', data)):
    if num == 0: continue
    if ESTA is not None and num != ESTA: continue
    num = int(num)
    titulo, titulo_titulo, _ = [t for t in titulos if t[2] <= num][-1]
    capitulo, capitulo_titulo, _ = [t for t in capitulos if t[2] <= num][-1]
    x = x.strip()
    x = x.strip('°°º\u00b0')
    declared_num = re.match(r'^([0-9]*).*', x).group(1)
    declared_num = 0 if declared_num == '' else int(declared_num)
    x = x.lstrip('.- 0123456789\u00b0[]*')
    #if ESTA is not None:
    #    print(rich_data(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo))
    #    break

    json_file = open(f'src/content/luc/LUC_articulo_{num}.json', "w")
    data = rich_data(num, declared_num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    json_file.write(json.dumps(data, indent=4))
    json_file.close()
    if ESTA is None:
        texto = data["textoModificado"]
        if len(texto) == 0:
            texto = data["textoOriginal"]
        texto = re.sub(r'^ART([íi]cULO|\.)?\s+[\.\d]+[º°]?\s*(bis|ter|qu[aá]ter|quinquies|sixties|septies|octies|undecies)?', '', texto, flags=re.I)
        texto = texto.lstrip('.-º—°').strip()
        texto = re.sub(r'^Incorpór[ea]se.*?[““]', '', texto, flags=re.MULTILINE | re.I | re.DOTALL)
        texto = re.sub(r'^ART([íi]cULO|\.)?\s+[\.\d]+[º°]?\s*(bis|ter|qu[aá]ter|quinquies|sixties|septies|octies|undecies)?', '', texto, flags=re.I)
        texto = texto.lstrip('.-º—°').strip()
        desc = re.split(r'[:\.\(]', texto)[0].replace("\n", " ").replace('"', '\\"')
        if len(desc) > 43:
            desc = desc[:40] + '...'
        pn = declared_num if declared_num > 0 else "sn"
        indice.write(f'''
- NRO_SECCION: {titulo}
  DESC_SECCION: {titulo_titulo}
  NRO_CAPITULO: {capitulo}
  DESC_CAPITULO: {capitulo_titulo}
  NRO_ARTICULO: "{num}"
  DESC_ARTICULO: "{f"{pn} - {desc}"}"
  RAW: {json.dumps(x)}
             '''.strip())
        indice.write('\n')