import re
import json
import sys
import os

def c(x):
    return x.replace('quáter', 'quater')

def rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'Derógase (?:la Ley|el Decreto Ley) N° ([0-9\.]+).*', x)
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
    m = re.match(r'(?:Deróguese|Derógan?se) (?:los artículos|el artículo) ([\d\s(?: bis),° y]+) (de la Ley|del Decreto-Ley|del Decreto de Necesidad y Urgencia|del Código Civil y Comercial)(?:.*?) N[º°] ([\d\.\/]+)\.?', x)
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
    art_old = [re.search(r'ART(?:[ÍI]CULO)?\.?\s*' + art + r'((?:.|\n)*?)\nART', old, re.I).groups()[0] for art in arts]
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

def rich_data_derogase_titulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    derogado = None
    if num == 199:
        with open('leyes/ley23905.txt') as fp:
            derogado = re.search(r'(TITULO VII\n.*?)TITULO VIII\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    elif num == 451:
        with open('leyes/ley26571.txt') as fp:
            derogado = re.search(r'(TITULO II\n.*?)TITULO III\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    elif num == 598:
        with open('leyes/ley23351.txt') as fp:
            derogado = re.search(r'(TITULO IV\n.*?)TITULO V\n', fp.read(), re.I | re.DOTALL).group(1).strip()
    elif num == 599:
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

def rich_data_sustituyese_articulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    if num == 550:
        x = x.replace('de Educación nacional.', 'de Educación nacional, por el siguiente:')
    m = re.match(r'(?:.*?)Sustit[uú]y[ae]se el artículo (\d+)[°º]?( (?:bis|ter|quater|quáter|quinquies|sixties|septies))?,? (?:(?:de )?(?:la )?[lL]ey|del Decreto-Ley)(?:.*?) N?[°º ]*([\d\.\/]+)(?:.*?) por el siguiente(?: texto)?:(.*)', x, re.MULTILINE|re.DOTALL)
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
    m = re.match(r'(?:.*?)Sustit[uú]yense los artículos ([\d\s,y]+) (?:(?:de )?la Ley|del Decreto-Ley)(?:.*?) N[°º ]*([\d\.\/]+)(?:.*?) por los siguientes(?: texto)?:(.*)', x, re.MULTILINE|re.DOTALL)
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
    m = re.match(r'(?:.*?)Derógase el inciso ([a-z0-9]+)\)? del artículo (\d+)[°º]? (del Decreto|de la Ley) N[°º] ([\d\.\/]+)(?:.*)', x, re.MULTILINE|re.DOTALL)
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

def rich_data_sustituyese_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el inciso ([a-z0-9]+)\)?[°º]? del artículo (\d+)[°º]? de la Ley (?:.*?)N[°º] ([\d\.]+)(?:.*),? por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
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
    if num == 355:
        ley = 'ccyc'
        art = '887'
        incs = {
            'a': 'sujetas a plazo tácito; si el plazo no está expresamente determinado, cuando resulta o no tácitamente de la naturaleza y circunstancias de la obligación, el acreedor debe interpelar al deudor para constituirlo en mora;',
            'b': 'sujetas a plazo indeterminado propiamente dicho; el juez a pedido de parte, lo debe fijar mediante el procedimiento más breve que prevea la ley local, a menos que el acreedor opte por acumular las acciones de fijación de plazo y de cumplimiento, en cuyo caso el deudor queda constituido en mora en la fecha indicada por la sentencia para el cumplimiento de la obligación.',
        }
    elif num == 375:
        ley = 'ccyc'
        art = '1514'
        incs = {
            'a': 'proporcionar, a satisfacción del franquiciado, información relevante sobre la evolución del negocio, en el país o en el extranjero;',
            'b': 'comunicar al franquiciado el conjunto de conocimientos técnicos, aun cuando no estén patentados, derivados de la experiencia del franquiciante y considerados por las partes aptos para producir los efectos del sistema franquiciado;',
        }
    elif num == 633:
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

def rich_data_194(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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

def rich_data_195(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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

def rich_data_196(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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
        "textoOriginal": 'ARTÍCULO ...- La existencia de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, sin importar su destino, sin el correspondiente respaldo documental o con documentación con irregularidades, será sancionada con una multa equivalente al importe que surja de la aplicación de lo, dispuesto en el segundo, tercer y cuarto párrafo del artículo 15, en proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco en existencia por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo cuando se de alguno de los siguientes supuestos:\n\na) La documentación sea apócrifa.b) Existan diferencias entre las cantidades de producto en existencia y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo, de la mercadería detectada y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el tenedor de las existencias de tabaco.',
        "textoModificado": 'ARTÍCULO ...- La existencia de tabaco despalillado, acondicionado, picado, en hebras o reconstituido o de polvo para la elaboración reconstituido, no comprendido en el artículo 18, sin importar su destino, sin el correspondiente respaldo documental o con documentación con irregularidades, será sancionada con una multa equivalente al importe que resulte de aplicar la alícuota dispuesta en el primer párrafo del artículo 15 sobre el precio que surja del relevamiento al que se refiere el artículo sin número agregado a continuación del artículo 2°, en proporción a la cantidad de cigarrillos que resulte de dividir el total de gramos de tabaco en existencia por ochenta centésimos (0,80), considerando el momento de la detección.\n\nA su vez, se procederá a la interdicción de la mercadería, disponiéndose su liberación con la acreditación del pago de la multa.\n\nSe considerará que existen irregularidades en la documentación de respaldo cuando se de alguno de los siguientes supuestos:\n\na) La documentación sea apócrifa.b) Existan diferencias entre las cantidades de producto en existencia y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las diferencias detectadas.\n\nc) Existan diferencias en el tipo, de la mercadería detectada y las que figuran en la documentación de respaldo, siendo en tal caso aplicables las disposiciones de este artículo sobre las unidades en las que se verifiquen dichas diferencias.\n\nA los fines de las sanciones establecidas en este artículo serán de aplicación las previsiones de la ley 11.683, texto ordenado en 1998 y sus modificaciones, resultando responsable el tenedor de las existencias de tabaco.',
    }

def rich_data_626(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
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
        "textoOriginal": 'ARTICULO 33. — OTROS REQUERIMIENTOS. Respecto a los vehículos se debe, además:\n\na) Los automotores ajustarse a los límites sobre emisión de contaminantes, ruidos y radiaciones parásitas. Tales límites y el procedimiento para detectar las emisiones son los que establece la reglamentación, según la legislación en la materia;\n\nb) Dotarlos de por lo menos un dispositivo o cierre de seguridad antirrobo;\n\nc) Implementar acciones o propaganda tendiente a disminuir el consumo excesivo de combustible;\n\nd) Otorgar la Cédula de Identificación del Automotor a todo vehículo destinado a circular por la vía pública, con excepción de los de tracción a sangre. Dicho documento detallará, sin perjuicio de su régimen propio, las características del vehículo necesarias a los fines de su control;\n\ne) Dichos vehículos además deben tener grabados indeleblemente los caracteres identificatorios que determina la reglamentación en los lugares que la misma establece. El motor y otros elementos podrán tener numeración propia;\n\nf) (Inciso vetado por art. 6° del Decreto N° 179/1995 B.O. 10/02/1995)\n\nARTICULO 40 bis) Requisitos para circular con bicicletas. Para poder circular con bicicleta es indispensable que el vehículo tenga:\n\na) Un sistema de rodamiento, dirección y freno permanente y eficaz;\n\nb) Espejos retrovisores en ambos lados;\n\nc) Timbre, bocina o similar;\n\nd) Que el conductor lleve puesto un casco protector, no use ropa suelta, y que ésta sea preferentemente de colores claros, y utilice calzado que se afirme con seguridad a los pedales;\n\ne) Que el conductor sea su único ocupante con la excepción del transporte de una carga, o de un niño, ubicados en un portaequipaje o asiento especial cuyos pesos no pongan en riesgo la maniobrabilidad y estabilidad del vehículo;\n\nf) Guardabarros sobre ambas ruedas;\n\ng) Luces y señalización reflectiva.',
        "textoModificado": 'ARTICULO 33. — OTROS REQUERIMIENTOS. Respecto a los vehículos se debe, además:\n\na) Los automotores ajustarse a los límites sobre emisión de contaminantes, ruidos y radiaciones parásitas. Tales límites y el procedimiento para detectar las emisiones son los que establece la reglamentación, según la legislación en la materia;\n\nc) Implementar acciones o propaganda tendiente a disminuir el consumo excesivo de combustible;\n\nd) Otorgar la Cédula de Identificación del Automotor a todo vehículo destinado a circular por la vía pública, con excepción de los de tracción a sangre. Dicho documento detallará, sin perjuicio de su régimen propio, las características del vehículo necesarias a los fines de su control;\n\ne) Dichos vehículos además deben tener grabados indeleblemente los caracteres identificatorios que determina la reglamentación en los lugares que la misma establece. El motor y otros elementos podrán tener numeración propia;\n\nf) (Inciso vetado por art. 6° del Decreto N° 179/1995 B.O. 10/02/1995)\n\nARTICULO 40 bis) Requisitos para circular con bicicletas. Para poder circular con bicicleta es indispensable que el vehículo tenga:\n\na) Un sistema de rodamiento, dirección y freno permanente y eficaz;\n\nb) Espejos retrovisores en ambos lados;\n\nc) Timbre, bocina o similar;\n\nd) Que el conductor lleve puesto un casco protector, no use ropa suelta, y que ésta sea preferentemente de colores claros, y utilice calzado que se afirme con seguridad a los pedales;\n\ne) Que el conductor sea su único ocupante con la excepción del transporte de una carga, o de un niño, ubicados en un portaequipaje o asiento especial cuyos pesos no pongan en riesgo la maniobrabilidad y estabilidad del vehículo;\n\ng) Luces y señalización reflectiva.',
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

def rich_data_switch(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    if num == 470:
        return rich_data_470(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if num == 192:
        return rich_data_192(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if num == 194:
        return rich_data_194(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if num == 195:
        return rich_data_195(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if num == 196:
        return rich_data_196(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if num == 626:
        return rich_data_626(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    opt = rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_titulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
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
    opt = rich_data_derogase_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_inciso_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_incisos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    if x.startswith('Sustit') and not x.startswith('Sustitúyese la denominación'):
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
    x = x[len(str(num)):]
    x = x.strip('°')
    x = x.strip('º')
    x = x.lstrip('.- ')
    x = re.sub(r'[^“]T[ÍI]TULO ([IXVL]+)(.*$)', '', x)
    x = re.sub(r'[^“]CAP[ÍI]TULO ([IXVL]+)(.*$)', '', x)

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
        texto = {
            9: 'Enajenación de las participaciones accionarias o de capital del Estado Nacional',
            11: 'Sociedades Anónimas',
            16: 'Operaciones de crédito público',
            17: 'Control de operaciones de crédito público',
            18: 'Control de operaciones de crédito público',
            19: 'Autoridad de control',
            20: 'Auditoría interna',
            21: 'Funciones de la Sindicatura General de la Nación',
            22: 'Requisitos para ser Síndico General de la Nación',
            23: 'Síndicos Generales Adjuntos',
            24: 'Requisitos para set Titular de la Oficina Anticorrupción',
            25: 'Funciones de la Oficina Anticorrupción',
            26: 'Anticorrupción en Poderes Legislativo y Judicial',
            27: 'Publicidad de los actos',
            28: 'Actividades prohíbidas para funcionarios públicos',
            33: 'Renegociación o rescisión de contratos',
            35: 'Cuestiones de competencia entre los Ministros',
            36: 'Incompetencia',
            37: 'Requisitos esenciales del acto administrativo',
            38: 'Manifestación del acto administrativo',
            39: 'Participación de usuarios y consumidores',
            40: 'Prohibiciones para la Administración',
            41: 'El silencio o la ambigüedad de la Administración',
            42: 'Notificación del acto administrativo',
            43: 'Presunción de legitimidad del acto administrativo',
            44: 'Nulidad absoluta del acto administrativo',
            45: 'Nulidad relativa del acto administrativo',
            46: 'Revocación o sustitución del acto administrativo irregular',
            47: 'Derogación de actos administrativos de alcance general',
            48: 'Saneamiento de actos administrativos',
            49: 'Prescripción de nulidad de actos administrativos',
            50: 'Impugnación judicial de actos administrativos particulares',
            51: 'Impugnación judicial de actos administrativos generales',
            52: 'Plazo de impugnación judicial de actos administrativos',
            53: 'Vía de impugnación judicial de actos administrativos',
            54: 'Demanda frente a silencio de la Administración',
            55: 'Acción de nulidad promovida por la Administración',
            56: 'Pronto despacho',
            57: 'Desobedencia del pronto despacho',
            58: 'Agotación de la vía administrativa',
            59: 'Derogación de la ley de Azúcar',
            60: 'Derogación de la ley de Libros',
            61: 'Ley de Defensa de la Competencia',
            62: 'Venta de entradas de espectáculos',
            63: 'Reventa de entradas deportivas',
            64: 'Tributo de mercaderías',
            65: 'Alícuota de tributo de mercaderías',
            66: 'Formulario de ingreso de productos',
            67: 'Derogación de la ley de Radiodifusión',
            68: 'Sucursales de aseguradores',
            69: 'Ramas de aseguradores',
            70: 'Requisitos planes de aseguradores',
            71: 'Primas de aseguradores',
            72: 'Plazos de control de aseguradores',
            73: 'Retención del importe de cuotas sociales',
            75: 'Inscripción en el Registro Público',
            76: 'Presentación de documentación',
            77: 'Verificación de Registros Públicos',
            78: 'Legajos',
            79: 'Requisitos del instrumento de constitución',
            80: 'Estipulaciones nulas',
            81: 'Créditos personales de socios',
            83: 'Acta de las deliberaciones',
            84: 'Reducción a uno del número de socios',
            85: 'Representación y administración de la Sociedad de Capital e Industria',
            86: 'Beneficios sociales del socio industrial',
            87: 'Denominación social de Sociedades de Responsabilidad Limitada',
            88: 'Aportes de Sociedad Anónima',
            89: 'Títulos de Sociedad Anónima',
            90: 'Títulos de Sociedad Anónima',
            91: 'Libros de registro de acciones',
            92: 'Transmisión de acciones',
            93: 'Votos',
            94: 'Adquisición de acciones emitidas por la sociedad',
            95: 'Enajenación de acciones',
            97: 'Administración de Sociedad Anónima',
            98: 'Términos del directorio',
            99: 'Elección del directorio',
            100: 'Consejo de vigilancia',
            101: 'Designación de síndicos',
            102: 'Fiscalización de Sociedades Anónimas Unipersonales',
            103: 'De la Sociedad anónima con participación Estatal Mayoritaria',
            104: 'Títulos de igual valor',
            105: 'Medios electrónicos de Registros Públicos',
            106: 'Suspensión de la movilidad de las prestaciones',
            107: 'Emisión de títulos públicos',
            108: 'Facturas de Crédito Electrónicas',
            110: 'Fomento desarrollo de la construcción de viviendas',
            111: 'Impedimentos para ser miembros del directorio de la Comisión Nacional de Valores',
            112: 'Directores de la Comisión Nacional de Valores',
            113: 'Régimen de Regularización Excepcional de Obligaciones Tributarias',
            114: 'Personas elegibles',
            115: 'Personas elegibles',
            116: 'Personas no elegibles',
            117: 'Efectos',
            118: 'Beneficios',
            119: 'Beneficios',
            120: 'Beneficios',
            121: 'Beneficios',
            122: 'Deudas en ejecución judicial',
            123: 'Importes exceptuados',
            124: 'Personas elegibles',
            125: 'Pesificación',
            126: 'Efectos',
            127: 'Efectos',
            128: 'Reglamentación',
            129: 'Vigencia',
            139: 'Reglas especiales según tipo de activo',
            155: 'Beneficios de sujetos que adhieran al Régimen de Regularización de Activos',
            156: 'Beneficios de sujetos que adhieran al Régimen de Regularización de Activos',
            157: 'Beneficios de sujetos que adhieran al Régimen de Regularización de Activos',
            158: 'Beneficios de sociedades que adhieran al Régimen de Regularización de Activos',
            172: 'Bienes a considerar',
            173: '',
            174: '',
            189: 'Precio imputable',
            190: 'Alícuota de cigarrillos',
            191: 'Impuesto mínimo de cigarrillos',
            192: 'Alícuota de tabacos',
            193: 'Alícuota de dispositivos administradores de nicotina con tabaco',
            194: 'Transporte de tabaco',
            195: 'Transporte de tabaco',
            196: 'Multa por tabaco irregular',
            197: 'Impuesto a Cigarrillos Electrónicos',
            198: 'Entrada en vigencia',
            199: 'Derogación del impuesto a la transferencia de inmuebles de personas físicas y sucesiones indivisas',
            200: 'Derechos de exportación sobre no gravadas',
            201: 'Derechos de exportación sobre gravadas por menos del 15%',
            202: 'Derechos de exportación sobre soja',
            203: 'Derechos de exportación sobre gravadas por más del 15%',
            204: 'Derechos de exportación sobre hidrocarburos y minería',
            205: 'Derechos de exportación sobre mercaderías vitivinícolas y aceite esencial del limón',
            206: 'Derechos de exportación sobre olivícola, arrocero, cueros bovinos, lácteo, frutícola, hortícola, porotos, lentejas, arveja, papa, ajo, garbanzos, miel, azúcar, yerba mate, té, equinos y lana',
            207: 'Delegación sobre el Poder Ejecutivo para reducir posiciones arancelarias',
            208: 'Discriminación de gravámenes en facturas',
            209: 'Prohibición de usar la palabra "gratuito"',
            210: 'Sujetos del impuesto PAIS',
            211: 'Distribución del producido del impuesto PAIS',
            214: 'Empleadores elegibles',
            215: 'Efectos',
            216: 'Derechos de los trabajadores',
            217: 'Plazo de regularización',
            218: 'Deudas elegibles',
            219: 'Efectos sobre las infracciones',
            220: 'Delegación sobre el Poder Ejecutivo de normas reglamentarias',
            221: 'Consolidación de títulos de deuda pública',
            222: 'Entidades excluidas',
            223: 'Efectos',
            224: 'Mantenimiento de créditos presupuestarios',
            225: 'Resolución de pedidos de mantenimiento',
            226: 'Trasferencia de los activos del Fondo de Garantía de Sustentabilidad',
            227: 'Derogación de la regulación del Fondo de Garantía de Sustentabilidad',
            228: 'Delegación sobre el Poder Ejecutivo de normas sobre regulación de industria de animales',
            229: 'Delegación sobre la Secretaría de Agricultura, Ganadería y Pesca sobre aspectos higiénico-sanitarios',
            230: 'Sistemas de control higiénico-sanitarios y ambiental',
            231: 'Limitación a la regulación provincial sobre exigencias sanitarias',
            232: 'Exclusividad de la Autoridad Reglamentaria Nacional para regular',
            233: 'Limitación al accionar provincial',
            234: 'Clausura de establecimientos',
            235: 'Infracciones',
            236: 'Autoridad de aplicación',
            237: 'Vías recursivas sobre las resoluciones',
            238: '',
            239: 'Obligación al Poder Ejecutivo de dictar un digesto reglamentario',
            240: 'Derogación de la Ley de Carnes',
            241: 'Adhesión a la Convención Internacional sobre la Protección de Nuevas Variedades Vegetales (1991)',
            242: 'Funciones de la autoridad de aplicación',
            243: 'Funciones del Consejo Federal Pesquero',
            244: 'Eliminación de la obligación desembarcar en muelles argentinos',
            245: 'Permisos de pesca',
            246: 'Cuota de captura por especie',
            247: 'Pesca de especies no cuotificadas',
            248: 'Permisos de pesca',
            249: 'Derecho de extracción',
            250: 'Aprobación de proyectos',
            251: 'Locación de buques de matrícula extranjera',
            252: 'Tripulación de los buques pesqueros',
            253: 'Permisos, autorizaciones de pesca y cuotas ya otorgadas',
            254: 'Delegación sobre el Poder Ejecutivo para reglamentar hidrocarburos',
            255: 'Objetivo de la delegación',
            256: 'Permisos',
            257: 'Permisos',
            258: 'Pautas de delegación',
            259: 'Delegación sobre el Poder Ejecutivo para reglamentar el regimen de importación de los hidrocarburos',
            260: 'Reconocimiento en beneficio de las provincias',
            261: 'Reconocimientos superficiales en busca de hidrocarburos',
            262: 'Permiso de exploración',
            263: 'Descubrimiento de hidrocarburos',
            264: 'Explotación No Convencional de Hidrocarburos',
            265: 'Autorización de transporte y/o procesamiento de hidrocarburos',
            266: 'Concesiones de explotación',
            267: 'Inversiones para la explotación',
            268: 'Vigencia de concesiones',
            269: 'Título de Autorizaciones de transporte y/o procesamiento',
            270: 'Autorizaciones de transporte y/o procesamiento',
            271: 'Autoridad de Aplicación y Registro',
            272: 'No exclusividad',
            273: 'Discriminación en el transporte y procesamiento',
            274: 'Normas subsidiarias',
            275: 'Procedimiento de adjudicación',
            276: 'Licitación',
            277: 'Concesiones de explotación existentes',
            278: 'Selección de propuesta',
            279: 'Oposición',
            280: 'Regalías',
            281: 'Regalías',
            282: 'Derechos',
            283: 'Derechos',
            284: 'Obligaciones',
            285: 'Deber de información',
            286: 'Empleo',
            287: 'Cesión',
            288: 'Fiscalización',
            289: 'Inspección y fiscalización',
            290: 'Nulidades',
            291: 'Caducidad',
            292: 'Arbitraje',
            293: 'Multas',
            294: 'Incumplimiento de oferentes',
            295: 'Áreas reservadas',
            296: 'Empresas estatales',
            297: 'Contrataciones',
            298: 'Delegación sobre el Poder Ejecutivo',
            299: 'Indemnizaciones',
            300: '',
            301: 'Importación de gas natural',
            302: 'Evaluación de la prestación del servicio',
            303: 'Recaudos',
            304: 'Fuero de impugnación',
            305: 'Audiencias públicas',
            306: 'Interés público nacional',
            307: 'Marco Regulatorio de Biocombustibles',
            308: 'Funciones de la autoridad de aplicación',
            309: 'Biocombustible',
            310: 'Registro de Biocombustible',
            311: 'Calidad',
            312: 'Cumplimiento',
            313: 'Mezclas mínimas obligatorias',
            314: 'Derogación de las leyes de Régimen de Regulación y Promoción para la Producción y uso sustentables de biocombustibles, Plan Nacional de Alconafta, Régimen de Promoción de la Producción de Bioetanol',
            315: 'Derogación de varios artículos del Marco Regulatorio de Biocombustibles',
            316: 'Ente Nacional Regulador del Gas y la Electricidad',
            317: 'Delegación sobre el Poder Ejecutivo de adecuación del Marco Regulatorio de la Energía Eléctrica',
            318: 'Delegación sobre el Poder Ejecutivo sobre los fondos fiduciarios del sector energético',
            319: 'Delegación sobre el Poder Ejecutivo para la legislación ambiental uniforme a nivel nacional',
            320: 'Delegación sobre el Poder Ejecutivo a asignar derechos de emisión de GEI a cada sector y subsector de la economía',
            321: 'Delegación sobre el Poder Ejecutivo a establecer anualmente límites de derechos de emisión de GEI',
            322: 'Delegación sobre el Poder Ejecutivo a monitorear el avance en el cumplimiento de las metas de emisiones de GEI',
            323: 'Delegación sobre el Poder Ejecutivo a establecer un mercado de derechos de emisión de GEI',
            324: 'Delegación sobre el Poder Ejecutivo a establecer las reglas del mercado de derechos de emisión de GEI',
            325: 'Derogación de beneficios aduaneros a la Policía de la Provincia de Buenos Aires',
            326: 'Entorpecimiento del normal funcionamiento de los transportes',
            328: 'Responsabilidad por manifestaciones',
            342: 'Intimidación o fuerza contra un funcionario público',
            343: 'Agravantes en la intimidación o fuerza contra un funcionario público',
            348: 'Derogación de la creación del INADI',
            349: 'Derogación de la nulidad por renuncia anticipada de honorarios',
            350: 'Gestión Colectiva de Derechos',
            351: 'Delegación sobre el Poder Ejecutivo a redactar el Regimen Legal de la Propiedad Intelectual',
            352: 'Divorcio administrativo',
            404: 'Extracciones de fondos depositados',
            405: 'Fondos depositados judicialmente',
            406: 'Perjuicios por órdenes de transferencias',
            407: 'Registro de Juicios Universales',
            408: 'Registro de Juicios Universales',
            409: 'Registro de Juicios Universales',
            410: 'Registro de Juicios Universales',
            411: 'Publicación de Edictos Judiciales',
            412: 'Archivo de los expedientes terminados y paralizados',
            413: 'Conformación del Archivo',
            414: 'Consulta del Archivo',
            415: 'Anotaciones en el Archivo',
            416: 'Registro de Juicios Universales',
            417: '',
            418: '',
            419: 'Depósitos judiciales',
            420: 'Depósitos judiciales',
            421: 'Depósitos judiciales',
            422: 'Transferencia del Registro de la Propiedad Inmueble a la Ciudad Autónoma de Buenos Aires',
            423: 'Sujetos del Registro de la propiedad inmueble',
            424: 'Documentos a inscribir',
            425: 'Requisitos',
            426: 'Verificación del Registro',
            427: 'Inmuebles inscriptos',
            428: 'Matriculación',
            429: 'Asiento de matriculación',
            430: 'Publicidad del Registro',
            431: 'Plazo de validez de la certificación',
            432: 'Copias de la documentación registral',
            433: 'Valor probatorio del asiento registral',
            434: 'Registro de las inhibiciones',
            435: 'Rectificación',
            436: 'Regulación',
            437: 'No restricción',
            438: 'Registro Nacional de Inhibiciones',
            439: 'Transferencia de la Justicia Nacional a la Ciudad Autónoma de Buenos Aires',
            440: 'Inspector General',
            441: 'Régimen sobre Procesos Sucesorios No Contenciosos',
            442: 'Régimen de Juicio por Jurados',
            443: 'Circunscripciones electorales',
            444: 'Normas electorales',
            445: 'Creación de circunscripciones electorales',
            446: 'Proyecto de diseño de las circunscripciones',
            447: 'Sorteo de las circunscripciones',
            448: 'Candidatos a diputados',
            449: 'Muerte, renuncia, separación, inhabilidad o incapacidad permanente de un/a Diputado/a Nacional',
            450: 'Representatividad de diputados',
            451: 'Derogación de la Ley de Primarias Abiertas Simultaneas y Obligatorias',
            452: 'Consejo de Seguimiento',
            453: 'Personería jurídico-política de las agrupaciones políticas',
            454: 'Alianzas',
            455: 'Conferederaciones',
            456: 'Autoridades partidarias',
            457: 'Candidatos no permitidos',
            461: 'Apelabilidad de las resoluciones de la Dirección Nacional Electoral',
            470: 'Derogación de artículos de la Ley de Financiamiento de los Partidos Políticos',
            473: 'Módulo electoral',
            474: 'Delegación sobre el Poder Ejecutivo a redactar el Código Electoral Nacional',
            475: 'Derogación de la Ley de Promoción de la construcción de hoteles de turismo Internacional',
            476: 'Derogación de la Ley de Promoción del turismo por medio de líneas de transporte',
            477: 'Derogación de artículos la Ley de Turismo',
            484: 'Certificado nacional de autorización para agencias de turismo estudiantil',
            485: 'Evaluación',
            486: 'Requisitos',
            487: 'Declaración jurada anual',
            488: 'Imposibilidad de brindar servicios',
            489: 'Cancelación del Certificado nacional de autorización para agencias de turismo estudiantil',
            490: 'Sumario previo',
            491: 'Plazos',
            492: 'Apelación',
            493: 'Prescripción',
            494: 'Prescripción',
            495: 'Prescripción',
            496: 'Prescripción',
            497: 'Quema',
            498: 'Prohibición',
            499: 'Comercialización de fertilizantes a granel',
            500: 'Proyectos de desmonte de bosques nativos',
            501: 'Integración del Fondo Nacional para el Enriquecimiento y la Conservación de los Bosques Nativos',
            506: 'Políticas Públicas',
            507: 'Asignación por Embarazo para Protección Social',
            518: 'Denominación Política pública de detección y asistencia a las madres embarazadas y sus hijos por nacer',
            524: 'Denominación Política pública de acompañamiento familiar',
            525: 'Objetivo',
            527: 'Tareas del Poder Ejecutivo Nacional',
            530: 'Denominación Política pública de fortalecimiento de primera infancia',
            535: 'Capacitación obligatoria',
            536: 'Autoridad de aplicación',
            537: 'Garantización de la implementación de las capacitaciones',
            538: 'Certificación de calidad',
            539: 'Autoridad',
            540: 'Publicidad de información',
            541: 'Transferencia del Consejo Nacional de Coordinación de Políticas Sociales',
            542: 'Funciones del Consejo Nacional de Coordinación de Políticas Sociales',
            543: 'Objetivos del Consejo Nacional de Coordinación de Políticas Sociales',
            544: 'Definición de criterios básicos de la carrera docente',
            545: 'Capacitación docente',
            546: 'Definición de criterios de regulación del sistema de formación docente',
            547: 'Bibliotecas escolares',
            548: 'Objeto de información y evaluación',
            549: 'Transparencia',
            550: 'Estudios a distancia híbridos',
            551: 'Convenio marco docente',
            553: 'Gratuidad de educación superior',
            554: 'Ingreso a la educación superior',
            555: 'Evaluaciones externas',
            556: 'Aporte del Estado nacional para las instituciones de educación superior',
            557: 'Potestades de las cooperadoras escolares',
            558: 'Dirección del INCAA',
            559: 'Deberes y atribuciones del Director Nacional de Cine y Artes Audiovisuales',
            560: 'Funciones de la Asamblea Federal',
            561: 'Funciones del Consejo Asesor',
            562: 'Películas nacionales',
            563: 'Certificado de exhibición',
            564: 'Integración del Fondo de Fomento Cinematográfico',
            565: 'Uso del Fondo de Fomento Cinematográfico',
            566: 'Limitación de largometrajes subsidiados',
            567: '',
            568: 'Lineamientos para determinar la aptitud de un proyecto aspirante a beneficiario',
            569: '',
            570: 'Cesión de subsidios',
            571: 'Concesión de entidad bancaria para créditos',
            572: 'Aplicación de los fondos del INCAA',
            573: 'Tasas',
            574: 'Nuevos créditos',
            575: 'Monto de créditos',
            576: 'Cinemateca Nacional',
            577: 'Vigencia',
            578: 'Derogación de artículos la Ley de fomento de la actividad cinematográfica nacional',
            582: 'Atribuciones del Director del INAMU',
            583: 'Mecanismos de promoción que podrá autorizar el INAMU',
            584: 'Presupuesto del INAMU',
            587: 'Derogación de la Ley Nacional del Teatro',
            588: '',
            589: 'Derogación de la Ley del Fondo Nacional de las Artes',
            590: '',
            591: 'Clasificación de las Bibliotecas Populares',
            592: 'Beneficios de las Bibliotecas Populares',
            593: 'Criterio de asignación de beneficios',
            594: 'Autoridad de aplicación',
            595: 'Creación de la Comisión Nacional Protectora',
            596: 'Composición Comisión Nacional Protectora',
            597: 'Miembros de la Comisión Nacional Protectora',
            598: 'Derogación del título de la Junta Representativa de Bibliotecas Populares',
            599: 'Derogación del título del Fondo Especial para Bibliotecas Populares',
            600: 'Derogación de la Ley de Museo, Biblioteca y Archivo del Trabajo y del Movimiento Obrero Argentino',
            601: 'Derogación de la Ley de Demoliciones de Teatros',
            602: 'Derogación de la Ley de Descuentos para Artistas en el Precio de Pasajes en Empresas Estatales de Transporte',
            606: 'Delegados sindicales en situación de disponibilidad',
            607: 'Tareas para agentes en situación de disponibilidad',
            608: 'Igualdad',
            609: 'Jubilación',
            610: 'Prohibición de campaña electoral en horas laborales',
            611: 'Sanciones',
            612: 'Cesantías',
            613: 'Exoneraciones',
            614: 'Prescripción',
            615: 'Exclusiones de Convención Colectiva de Trabajo',
            616: 'Cuotas de solidaridad',
            617: 'Descuento por huelga',
            618: 'Riesgo por salud mental',
            619: 'Promoción de acciones de inclusión',
            620: 'Internación involuntaria',
            621: 'Representación por internación involuntaria',
            622: 'Alta, externación o permisos de salida',
            623: 'Centros médicos',
            624: 'Instituciones de internación',
            625: 'Conformación de Órgano de Revisión',
            626: 'Otros requerimientos',
            627: 'Vehículo autodirigido',
            628: 'Autorización de vehículos autodirigidos',
            629: 'Delegación sobre el Poder Ejecutivo para autorizar vehículos autodirigidos',
            630: 'Revisión técnica obligatoria',
            631: 'Exhibición de documentos',
            632: 'Condiciones para conducir',
            633: 'Requisitos para circular',
            634: 'Peajes',
            635: 'Transporte de carga',
            636: 'Obligaciones',
            639: 'Fines',
            640: 'Registro Único del Transporte Automotor',
            641: 'Creación del Régimen de Incentivo para Grandes Inversiones',
            642: 'Autoridad de aplicación',
            643: 'Concesiones de obra pública',
            644: 'Financiación del concesionario',
            645: 'Otorgamiento de obras públicas',
            646: 'Contenido del contrato de concesión',
            647: 'Intangibilidad de la ecuación económico-financiera',
            648: 'Extinción del contrato por razones de interés público',
            649: 'Mecanismos de prevención y solución de controversias',
            650: 'No aplicación de otras leyes',
            651: 'Normalización',
            652: 'Derogación de varios artículos de la Ley de Obras Públicas',
            653: 'Autoridad de aplicación',
            654: 'Ratificación del Decreto de Necesidad y Urgencia N° 70/23',
            655: 'Anexos',
            656: '',
            657: '',
            658: '',
            659: '',
            660: 'Facultad de reasignación de competencias',
            661: '',
            663: 'Entrada en vigencia',
            664: '',
        }.get(num, texto)
        desc = re.split(r'[:\.\(]', texto)[0].replace("\n", " ").replace('"', '\\"')
        indice.write(f'''
- NRO_SECCION: {titulo}
  DESC_SECCION: {titulo_titulo}
  NRO_CAPITULO: {capitulo}
  DESC_CAPITULO: {capitulo_titulo}
  NRO_ARTICULO: {num}
  DESC_ARTICULO: "{desc}"
             '''.strip())
        indice.write('\n')