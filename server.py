# -*- coding: utf-8 -
from wsgiref.validate import validator
from scrap import get_sitio
import re
import redis
import time

DIGITS = re.compile('\d+')
cache = redis.Redis(host='localhost', port=6379, db=0)

def donde(cedula):
    """
    Tries to take the info from the redis cache
    or triggers a scrap if it's not there yet
    """
    cached_sitio = cache.get(cedula)
    if cached_sitio is not None:
        return cached_sitio
    else:
        sitio =  get_sitio(cedula, text=True)
        cache.set(cedula, sitio) 
        return sitio

#@validator
def app(environ, start_response):
    """Simplest possible application object"""
    t1 = time.time()
    path_info = environ['PATH_INFO']
    digitos= DIGITS.findall(path_info)
    data = '{"error": "Cagada"}'
    status = '200 OK'
    if len(digitos)==1:
        cedula = digitos[0]
        data =donde(cedula)
    t2 = time.time()
    duration = str("%0.3f ms" % ((t2-t1)*1000.0,))
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data))),
        ('Duration', duration)
    ]
    start_response(status, response_headers)
    return iter([data])
