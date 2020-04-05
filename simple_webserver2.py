# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 15:49:50 2020

@author: pietertpt
"""
import RPi.GPIO as GPIO
import os
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '10.0.0.200'  # Change this to your Raspberry Pi IP address
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
           <body style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {temp}</p>
           <p>Turn All Off: <a href="/on">On</a> <a href="/off">Off</a></p>
           <p>Light One: {lightOne}</p>
           <p>Light Two: {lightTwo}</p>
           <p>Light Three: {lightThr}</p>
           <p>Light Four: {lightFou}</p>
           <div id="led-status"></div>
           <script>
               document.getElementById("led-status").innerHTML="{led}";
           </script>
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
            lightOne='<a href="/offOne">Off</a>'
        else:
            lightOne='<a href="/onOne">On</a>'
            
        lightTwo = ''
        if GPIO.input(16):
            lightTwo='<a href="/offTwo">Off</a>'
        else:
            lightTwo='<a href="/onTwo">On</a>'
            
        lightThr = ''
        if GPIO.input(20):
            lightThr='<a href="/offThr">Off</a>'
        else:
            lightThr='<a href="/onThr">On</a>'
            
        lightFou = ''
        if GPIO.input(21):
            lightFou='<a href="/offFou">Off</a>'
        else:
            lightFou='<a href="/onFou">On</a>'

        self.wfile.write(html.format(temp=temp[5:], led=status, lightOne=lightOne, lightTwo=lightTwo, lightThr=lightThr, lightFou=lightFou).encode("utf-8"))
        
        
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()




