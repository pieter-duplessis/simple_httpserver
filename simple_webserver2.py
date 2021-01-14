# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 15:49:50 2020

@author: pietertpt
"""
import RPi.GPIO as GPIO
import os
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.2.200'  # Change this to your Raspberry Pi IP address
host_port = 8000


class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """
    

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        
        
        html = '''
           <html>
<head>
<title>RPi Automation Page</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
</head>
<body data-spy="scroll" data-target=".site-navbar-target" data-offset="300">
    <div class="container">
        <h1>RPi Automation</h1>
        <p>Current GPU temperature is {temp}</p>

        <p>Turn All Off: <a type="button" class="btn btn-success" href="/on">On</a> <a type="button" class="btn btn-danger" href="/off">Off</a></p>
        <p>Light Main Bedroom: {lightThr}</p>
        <p>Light Red: {lightFou}</p>
        <p>Light One: {lightOne}</p>
        <p>Light Two: {lightTwo}</p>
        <div id="led-status"></div>
    </div>

<script>
    document.getElementById("led-status").innerHTML="{led}";
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
</body>
</html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        if self.path=='/on':
            GPIO.output(12, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
        elif self.path=='/off':
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.HIGH)
        elif self.path=='/oneOne':
            GPIO.output(12, GPIO.HIGH)
        elif self.path=='/offOne':
            GPIO.output(12, GPIO.LOW)
        elif self.path=='/onTwo':
            GPIO.output(16, GPIO.HIGH)
        elif self.path=='/offTwo':
            GPIO.output(16, GPIO.LOW)
        elif self.path=='/onThr':
            GPIO.output(20, GPIO.HIGH)
        elif self.path=='/offThr':
            GPIO.output(20, GPIO.LOW)
        elif self.path=='/onFou':
            GPIO.output(21, GPIO.HIGH)
        elif self.path=='/offFou':
            GPIO.output(21, GPIO.LOW)
        
        lightOne = ''
        if GPIO.input(12):
            lightOne='<a type="button" class="btn btn-danger" href="/offOne">Off</a>'
        else:
            lightOne='<a type="button" class="btn btn-success" href="/onOne">On</a>'
            
        lightTwo = ''
        if GPIO.input(16):
            lightTwo='<a type="button" class="btn btn-danger" href="/offTwo">Off</a>'
        else:
            lightTwo='<a type="button" class="btn btn-success" href="/onTwo">On</a>'
            
        lightThr = ''
        if GPIO.input(20):
            lightThr = '<a type="button" class="btn btn-danger" href="/offThr">Off</a>'
        else:
            lightThr='<a type="button" class="btn btn-success" href="/onThr">On</a>'
            
        lightFou = ''
        if GPIO.input(21):
            lightFou='<a type="button" class="btn btn-danger" href="/offFou">Off</a>'
        else:
            lightFou='<a type="button" class="btn btn-success" href="/onFou">On</a>'

        self.path = host_name
        self.wfile.write(html.format(temp=temp[5:], led=status, lightOne=lightOne, lightTwo=lightTwo, lightThr=lightThr, lightFou=lightFou).encode("utf-8"))
        
        
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()




