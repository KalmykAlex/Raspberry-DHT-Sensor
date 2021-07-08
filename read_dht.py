import time
import json
import board
import logging
import argparse
import socket
import adafruit_dht

# Logging Config
logging.basicConfig(filename='/home/pi/dht_sensor/read_dht.log', level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')


# Argparse Init
#parser = argparse.ArgumentParser(description='Read temperature and humidity from DHT sensor.')
#parser.add_argument('-d', type=str, help='DHT Sensor (dht11 or dht22)')
#args = parser.parse_args()

# Host Config
HOST = '172.16.1.239'
LOCATION = '322'
DATA_PIN = board.D4

# UDP Communication Info
SERVER_IP = '172.18.2.4'
SERVER_PORT = 6969
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
NETWORK_WAIT = 15  # seconds to wait for network connectivity

# Sensor selection
#if args.d == 'dht11':
#    dhtDevice = adafruit_dht.DHT11(DATA_PIN)
#elif args.d == 'dht22':
#    dhtDevice = adafruit_dht.DHT22(DATA_PIN)

logging.info('read_dht.py has started')
dhtDevice = adafruit_dht.DHT11(DATA_PIN, use_pulseio=False)


# Main Loop
while True:
    try:
        dht_data = {
            'host': HOST,
            'location': LOCATION,
            'temperature': dhtDevice.temperature,
            'humidity': dhtDevice.humidity/100
            }
        encoded_dht_data = json.dumps(dht_data).encode('utf-8')
        print(dht_data)
        sock.sendto(encoded_dht_data, (SERVER_IP, SERVER_PORT))
    except RuntimeError as error:
        print(error)
        time.sleep(5)
        continue
    except OSError as error:
        if error.errno == 101:
            logging.error(f'Network Error: {SERVER_IP} is unreacheable')
            logging.info(f'waiting {NETWORK_WAIT} seconds for network connectivity')
            time.sleep(NETWORK_WAIT)
        else:
            logging.error(f'OSError: {error}')
        time.sleep(5)
        continue
    except Exception as error:
        logging.error(f'{error}')
        dhtDevice.exit()
        raise error
    time.sleep(5)
