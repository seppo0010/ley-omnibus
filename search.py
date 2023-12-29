import re
import json
import os

def rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'Derógase la Ley N° ([0-9\.]+).*', x)
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
    m = re.match(r'Derógan?se (?:los artículos|el artículo) ([\d\s,° y]+) (de la Ley|del Decreto-Ley) N° ([\d\.\/]+)\.?', x)
    if m is None: return None
    arts, lod, ley = m.groups()
    arts = [art.strip() for art in arts.replace('\n', ' ').replace('°', '').replace('y', '').replace(',', '').split(' ')]
    arts = [art for art in arts if art != '']
    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/ley{ley}.txt') as fp:
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

def rich_data_sustituyese_articulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el artículo (\d+)[°º]? (?:de la Ley|del Decreto-Ley)(?:.*?) N[°º] ([\d\.\/]+)(?:.*?) por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    art, ley, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    ley = ley.replace('.', '').replace('/', '-')
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
    m = re.match(r'(?:.*?)Sustitúyese el (primer|segundo|tercer|cuarto) párrafo del artículo (\d+)[°º]? de la (Ley|Decreto)(?:.*?) (?:N[°º] )?([\d\.\/]+)(?:.*?) por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    par, art, lod, ley, art_new = m.groups()
    art_new = art_new.replace('“', '')
    art_new = art_new.replace('”', '')
    art_new = art_new.strip()

    ley = ley.replace('.', '').replace('/', '-')
    with open(f'leyes/{"ley" if lod == "Ley" else "decreto"}{ley}.txt') as fp:
        old = fp.read() + '\nART'

    art_old = re.search(r'\n(ART(?:[ÍI]CULO)?\.?\s*' + art + r'(?:.|\n)*?)\nART', old, re.I).groups()[0]
    paragraphs = re.split(r'\n+', art_old)
    paragraphs[{
        'primer': 0,
        'segundo': 1,
        'tercer': 2,
        'cuarto': 3,
    }[par]] = art_new
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

def rich_data_sustituyese_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    m = re.match(r'(?:.*?)Sustitúyese el inciso ([a-z])\)? del artículo (\d+)[°º]? de la Ley N[°º] ([\d\.]+),? por el siguiente:(.*)', x, re.MULTILINE|re.DOTALL)
    if m is None: return None
    inc, art, ley, inc_new = m.groups()
    inc_new = inc_new.replace('“', '')
    inc_new = inc_new.replace('”', '')
    inc_new = inc_new.strip()

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
        "textoModificado": re.sub(inc + r'[\)\.].*', inc_new, art_old),
    }

def rich_data(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo):
    opt = rich_data_derogase_ley(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_derogase_articulos(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo_dnu(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo_cpn(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_articulo_ccyc(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_parrafo(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
    opt = rich_data_sustituyese_inciso(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo)
    if opt is not None: return opt
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

ESTA = None
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

    if ESTA is None:
        indice.write(f'''
- NRO_SECCION: {titulo}
  DESC_SECCION: {titulo_titulo}
  NRO_CAPITULO: {capitulo}
  DESC_CAPITULO: {capitulo_titulo}
  NRO_ARTICULO: {num}
  DESC_ARTICULO: ""
             '''.strip())
        indice.write('\n')
    json_file = open(f'src/content/luc/LUC_articulo_{num}.json', "w")
    json_file.write(json.dumps(rich_data(num, x, titulo, titulo_titulo, capitulo, capitulo_titulo), indent=4))
    json_file.close()
