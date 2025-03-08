# DCN Lab 3, Tai Wan Kim
# Authoritative Server

from socket import *

AS_HOST = "0.0.0.0"
AS_PORT = 53533
FILE_NAME = "records.txt" # file to permanently store DNS records

def load_records():
    records_map = {}
    
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                record = line.strip().split(',')
                name, value, _type, ttl = record
                records_map[name] = (value, _type, ttl)  
    
    except FileNotFoundError:
        raise Exception("Failed to open file: ", FILE_NAME)
    
    return records_map

def add_record(record):
    print("add record to file...")

    with open(FILE_NAME, "a") as file:
        file.write(record + "\n")

def handle_registration(decoded):
    print("handling registration...")

    split = decoded.split("\n")

    _type = split[0].split("=")[1]
    name = split[1].split("=")[1]
    value = split[2].split("=")[1]
    ttl = split[3].split("=")[1]

    record = f"{name},{value},{_type},{ttl}"
    add_record(record)

    return "record registered"

def handle_query(decoded, records):
    print("handling query...")

    split = decoded.split("\n")

    _type = split[0].split("=")[1]
    name = split[1].split("=")[1]

    if name in records:
        value, _type, ttl = records[name]
        response = f"TYPE={_type}\nNAME={name}\nVALUE={value}\nTTL={ttl}\n"

        return response
    
    else:
        return "Record not found"

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((AS_HOST, AS_PORT))

print("AS running on port ", AS_PORT)

try:
    while True:
        records = load_records()

        print("waiting for requests...")

        msg, addr = sock.recvfrom(1024)
        decoded = msg.decode()

        print("request received: ", decoded)

        if "VALUE" in decoded:
            response = handle_registration(decoded)

        else:
            response = handle_query(decoded, records)

        print(response)
        sock.sendto(response.encode(), addr)

except KeyboardInterrupt:
    print("Keyboard Interrupt")

finally:
    sock.close()