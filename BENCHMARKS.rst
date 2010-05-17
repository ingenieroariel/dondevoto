Prueba simple con 20 requests al servidor de la registraduría y a nuestro servicio:

.. code-block::bash

    ab -n 20 http://www3.registraduria.gov.co/censo/_censoresultado.php?nCedula=70041053


This is ApacheBench, Version 2.3 <$Revision: 655654 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking www3.registraduria.gov.co (be patient).....done


Server Software:        Microsoft-IIS/6.0
Server Hostname:        www3.registraduria.gov.co
Server Port:            80

Document Path:          /censo/_censoresultado.php?nCedula=70041053
Document Length:        6559 bytes

Concurrency Level:      1
Time taken for tests:   37.819 seconds
Complete requests:      20
Failed requests:        0
Write errors:           0
Total transferred:      135080 bytes
HTML transferred:       131180 bytes
Requests per second:    0.53 [#/sec] (mean)
Time per request:       1890.940 [ms] (mean)
Time per request:       1890.940 [ms] (mean, across all concurrent requests)
Transfer rate:          3.49 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       82   95   8.4     96     109
Processing:   939 1795 1749.2   1094    5875
Waiting:      739 1597 1750.7    909    5682
Total:       1026 1891 1746.2   1203    5962

Percentage of the requests served within a certain time (ms)
  50%   1203
  66%   1234
  75%   1236
  80%   1238
  90%   5942
  95%   5962
  98%   5962
  99%   5962
 100%   5962 (longest request)

.. code-block::bash

    ab -n 20 http://endondevoto.com/api/70041053.json


This is ApacheBench, Version 2.3 <$Revision: 655654 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking endondevoto.com (be patient).....done


Server Software:        nginx/0.7.65
Server Hostname:        endondevoto.com
Server Port:            80

Document Path:          /api/70041053.json
Document Length:        120 bytes

Concurrency Level:      1
Time taken for tests:   0.394 seconds
Complete requests:      20
Failed requests:        0
Write errors:           0
Total transferred:      5280 bytes
HTML transferred:       2400 bytes
Requests per second:    50.76 [#/sec] (mean)
Time per request:       19.701 [ms] (mean)
Time per request:       19.701 [ms] (mean, across all concurrent requests)
Transfer rate:          13.09 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        9   10   0.4     10      11
Processing:    10   10   0.3     10      11
Waiting:       10   10   0.2     10      11
Total:         19   20   0.6     20      22

Percentage of the requests served within a certain time (ms)
  50%     20
  66%     20
  75%     20
  80%     20
  90%     20
  95%     22
  98%     22
  99%     22
 100%     22 (longest request)


Diferencia en performance:
Requests per second:
Ellos:    0.53 (PHP + Base Datos) (Una persona cada dos segundos) 
Nosotros: 50.75 (Python + Redis - Todo en RAM)  (50 personas por segundo)

100 veces más eficiente!
