import pycurl
import urllib2
from BeautifulSoup import BeautifulSoup
import json

BASE_URL="http://www3.registraduria.gov.co/censo/_censoresultado.php?nCedula=%s"
CEDULAS="cedulas.txt"
OUTPUT="votacion.json"
USER_AGENT="Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"

class Info:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf

    def data(self):
        soup = BeautifulSoup(self.contents)
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
    url = BASE_URL % cedula
    t = Info()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.USERAGENT, USER_AGENT)
    c.setopt(c.WRITEFUNCTION, t.body_callback)
    c.perform()
    c.close()
    data = {cedula: t.data()}
    if not text:
        return data
    else:
        return json.dumps(data) 

if __name__=="__main__":
    salida = {}
    for cedula in open(CEDULAS):
        salida.update(get_sitio(cedula))

    out = open(OUTPUT,'w')
    json.dump(salida, out)
    out.close()
