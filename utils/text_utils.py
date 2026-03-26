import unicodedata

def normalize_header(s):
    '''Normaliza el texto de encabezados'''
    if s is None:
        return ""
    s = str(s).strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join([c for c in s if not unicodedata.combining(c)])
    s = s.replace("º", "o").replace("nro", "numero").replace("n°", "numero")
    s = s.replace(".", " ").replace(",", " ").replace("-", " ").replace("/", " ")
    s = " ".join(s.split())
    return s