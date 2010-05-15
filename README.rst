dondevoto - Código detrás de endondevoto.com
============================================

It's all about performance

Componentes
-----------

 * ``Nginx``: Sirve los archivos estáticos y es el proxy por un unix socket al servidor de aplicaciones
 * ``Python/WSGI/Gunicorn``: Pequeña aplicación en WSGI que busca los datos de votación basado en la cédula
 * ``Redis``: Base de datos en memoria que almacena la información de votación. (9GB de RAM para 30 millones de registros)
 * ``Ubuntu``: Ubuntu 10.04 Lucid Lynx, recien salido del horno
 * ``Amazon EC2``: 15 GB de ram, 8 cores de procesamiento, 1.69 Tera Bytes de disco duro ( de los que usamos menos de un Giga), 64-bit= $1200 pesos la hora!

Arquitectura fácilmente escalable simplemente agregando más servidores de a $1200 la hora.
