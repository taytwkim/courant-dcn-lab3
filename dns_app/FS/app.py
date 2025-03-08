# DCN Lab 3, Tai Wan Kim
# Fibonacci Server

from flask import Flask, request, jsonify
from socket import *
import requests
import logging

FS_HOST = "0.0.0.0"
FS_PORT = 9090

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/register', methods=['PUT'])
def register():
    logging.info("Registering domain...")

    data = request.json
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']

    if not all([hostname, ip, as_ip, as_port]):
        logging.warning("Request missing a parameter")
        return jsonify({"error": "Missing parameter"}), 400

    logging.info("hostname: %s, ip: %s, as_ip: %s, as_port: %s", hostname, ip, as_ip, as_port)

    msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket(AF_INET, SOCK_DGRAM)
    
    try:
        sock.sendto(msg.encode(), (as_ip, int(as_port)))
        return "Registration Success", 201

    except requests.exceptions.RequestException as e:
        logging.error("Error reaching AS: %s", str(e))
        return jsonify({"error": "Error reaching AS"}), 500
    
    finally:
        sock.close()
  
def fib(n):
    if n == 1:
        return 0
    
    elif n == 2:
        return 1
    
    return fib(n-1) + fib(n-2)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    logging.info("Computing fibonacci...")
    
    number = request.args.get('number')

    if not number:
        return jsonify({"error": "cannot read number"}), 400
    
    n = int(number)

    if n <= 0:
        return jsonify({"error": "invalid number provided"}), 400

    res = fib(n)

    logging.info("fib %s is %s", n, res)

    return jsonify({"fibonacci": res}), 200

if __name__ == '__main__':
    logging.info("US running on port 8080")
    app.run(host=FS_HOST, port=FS_PORT)
