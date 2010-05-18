# -*- coding: utf-8 -
import urllib2
from BeautifulSoup import BeautifulSoup
# Use simplejson or Python 2.6 json, prefer simplejson.
try:
    import simplejson as json
except ImportError:
    import json

BASE_URL="http://www3.registraduria.gov.co/censo/_censoresultado.php?nCedula=%s"
CEDULAS="cedulas.txt"
OUTPUT="votacion.json"
USER_AGENT="Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"

def parse(data):
    """ Toma la página completa y le saca la información relevante"""
    soup = BeautifulSoup(data)
    table = soup("td")
    items=[]
    for entry in table:
        try:
            if entry.string is not None:
                items.append(entry.string.strip())
        except AttributeError:
            pass
    return items


def get_sitio(cedula, text=False):
    """ Se conecta con la registraduría y entrega un objecto JSON con la info"""
    url = BASE_URL % cedula
    request = urllib2.Request(url)
    opener = urllib2.build_opener()  
    # sino se agrega un USER_AGENT valido, el servidor se queja porque no
    # soporta frames :(
    request.add_header('User-Agent', USER_AGENT)
    data = opener.open(request).read()
    sitio = {cedula: parse(data)}
    if not text:
        return sitio
    else:
        return json.dumps(sitio) 

if __name__=="__main__":
    salida = {}
    for cedula in open(CEDULAS):
        salida.update(get_sitio(cedula))

    out = open(OUTPUT,'w')
    json.dump(salida, out)
    out.close()
