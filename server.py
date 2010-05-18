# -*- coding: utf-8 -
from wsgiref.validate import validator
from scrap import get_sitio
import re
import redis
import time
import os
import mimetypes
from redis import ConnectionError
DIGITS = re.compile('\d+')
BLOCK_SIZE = 16 * 4096
INDEX_FILE= 'index.html'
APP_PATH='api'
STATIC_DIR=os.getcwd() + '/static'

try:
    cache = redis.Redis(host='localhost', port=6379, db=0)
except:
    cache = None


def donde(cedula):
    """
    Tries to take the info from the redis cache
    or triggers a scrap if it's not there yet
    """
    try:
        sitio = cache.get(cedula)
        if sitio is None:
            sitio =  get_sitio(cedula, text=True)
            cache.set(cedula, sitio) 
    except ConnectionError:
        #redis no esta funcionando, mandémoslo directo
        sitio = get_sitio(cedula, text=True)
    return sitio

def iter_and_close(file_like, block_size):
    """Yield file contents by block then close the file."""
    while 1:
        try:
            block = file_like.read(block_size)
            if block: yield block
            else: raise StopIteration
        except StopIteration, si:
            file_like.close()
            return 

def serve_static(path_info, environ, start_response):
    full_path = os.path.abspath(STATIC_DIR + path_info)
    if os.path.isdir(full_path):
        full_path = os.path.abspath( os.path.join(full_path, INDEX_FILE ))
    if not os.path.isfile(full_path):
        start_response("404 Not Found", [('Content-Type', 'text/plain')])
        return ""
    content_type = mimetypes.guess_type(full_path)[0] or 'text/plain'
    file_like = open(full_path, 'rb')
    start_response("200 OK", [('Content-Type', content_type)])
    way_to_send = environ.get('wsgi.file_wrapper', iter_and_close)    
    return way_to_send(file_like, BLOCK_SIZE) 

def app(environ, start_response):
    """Simplest possible application object"""
    t1 = time.time()
    path_info = environ['PATH_INFO']
    if APP_PATH not in path_info:
        #Mínimo están intentando usarlo para servir
        #static files, no estoy de acuerdo, usen nginx.
        #pero ya que soy tan chevere, ahi les dejo un script
        #para servir static files :)
        return serve_static(path_info, environ, start_response)
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

if __name__=="__main__":
    from wsgiref.simple_server import make_server
    print "Prendiendo el servidor, abre tu navegador y ve a http://localhost:9999"
    make_server('localhost', 9999, app).serve_forever()
