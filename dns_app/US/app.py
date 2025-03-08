# DCN Lab 3, Tai Wan Kim
# User Server

from flask import Flask, request, jsonify
from socket import *
import requests
import logging

US_HOST = "0.0.0.0"
US_PORT = 8080

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    logging.info("GET request received")

    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        logging.warning("Request missing a parameter")
        return jsonify({"error": "Missing parameter"}), 400

    logging.info("Querying AS to resolve hostname...")

    msg = f"TYPE=A\nNAME={hostname}\n"

    sock = socket(AF_INET, SOCK_DGRAM)

    try:
        sock.sendto(msg.encode(), (as_ip, int(as_port)))
        as_response, _ = sock.recvfrom(1024)

    except requests.exceptions.RequestException as e:
        logging.error("Error reaching AS: %s", str(e))
        return jsonify({"error": "Error reaching AS"}), 500
    
    finally:
        sock.close()

    decoded = as_response.decode()
    split = decoded.split("\n")

    if len(split) < 3 or "NAME=" not in split[1] or "VALUE=" not in split[2]:
        logging.error("Failed to reach AS")
        return jsonify({"error": "Failed to reach AS"}), 500

    name = split[1].split('=')[1]
    ip = split[2].split('=')[1]

    logging.info("Received response from AS, Name: %s, IP: %s", name, ip)

    logging.info("Sending request to FS...")

    try:
        fs_response = requests.get(f"http://{ip}:{fs_port}/fibonacci?number={number}")
        return fs_response.text, 200
    
    except requests.exceptions.RequestException as e:
        logging.error("Error reaching FS: %s", str(e))
        return jsonify({"error": "Error reaching FS"}), 500

if __name__ == '__main__':
    logging.info("US running on port %s", US_PORT)
    app.run(host=US_HOST, port=US_PORT)
