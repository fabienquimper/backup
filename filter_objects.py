import pandas as pd
import numpy as np
import argparse
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# Configuration
CONFIG_NETWORK_PORT_FOR_SEQUENCE = 8005
CONFIG_NETWORK_PORT_FOR_PROCESSING = 8003
CONFIG_IS_SEND_TO_PROCESSING = True
CONFIG_PROCESSING_MS_SLEEP_BETWEEN_IMAGE = 150


######## Configure the server / client
# Set-up OSC server
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="localhost", help="The ip to listen on")
parser.add_argument("--port", type=int, default=CONFIG_NETWORK_PORT_FOR_SEQUENCE, help="The port to listen on")
args = parser.parse_args()
# OSC client
clientSequence = udp_client.SimpleUDPClient(args.ip, CONFIG_NETWORK_PORT_FOR_SEQUENCE)
clientProcessing = udp_client.SimpleUDPClient(args.ip, CONFIG_NETWORK_PORT_FOR_PROCESSING)

# Reception OSC message (mode)
def print_objects(unused_addr, args):
    print("Mode received: [{0}]".format(args[0]))
    objects_selector(args[0])
# Reception OSC message (list)
def print_list(unused_addr, args):
    print("List received: [{0}]".format(args))
dispatcher = dispatcher.Dispatcher()

def filter_value(unused_addr, args):
    print("Filter value: [{0}]".format(args))
def filter_reset(unused_addr, args):
    print("Filter reset: [{0}]".format(args))
def filter_min_max(unused_addr, args):
    print("Filter min-max: [{0}]".format(args))
# Id mode has been received (from another OSC message)
dispatcher.map("/control/controler/sequence", print_objects)
dispatcher.map("/control/controler/filter/value", filter_value)
dispatcher.map("/control/controler/filter/reset", filter_reset)
dispatcher.map("/control/controler/filter/min-max", filter_min_max)
dispatcher.map("/control/controler/filter/result", print_list)
# Start the server
server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher) 
#### END OF OSC CONFIGURATION


# Read CSV
df = pd.read_csv('data-0-4_tab_header_cleaned.csv', header=[0], sep='\t') 

print('All columns names:')
print(list(df.columns))
#'Jour', 'Annee', 'Mois', 'Jour.1', 'Depart', 'Arrivee', 'Pays', 'Km_jours', 'Km_cumule', 'Altitude', 'Lat_degres', 'Lat_minutes', 'Lat_decimale', 'Lat_radian', 'Long_degres', 'Long_minutes', 'Long_decimale', 'Long_radian', 'km_vol_oiseau', 'km_corde', 'km_segment', 'km_cumule', 'Unnamed: 22', 'Objet', 'Lieu', 'Contexte', 'Catégorie', 'Post', 'Jour xxx', 'Titre', 'Unnamed: 30', 'Poids', 'Taille', 'Couleur', 'Matiere', 'Origine', 'Unnamed: 36', 'Date', 'Coordonnees'

#print('Print all datas')
#print(df)

def objects_selector(mode):
    # Mode 1 select all object where color is up to 11 and altitude >= 4000m
    result = df

    if mode == "1":
        result = df.sort_values(['Jour'], ascending=[1])
    elif mode == "2":
        result = df.sort_values(['Altitude'], ascending=[1])
    elif mode == "3":
        result = df.sort_values(['Km_jours'], ascending=[1])
    elif mode == "4":
        result = df.sort_values(['Poids'], ascending=[1])
    elif mode == "5":
        result = df.sort_values(['Taille'], ascending=[1])
    elif mode == "6":
        result = df.sort_values(['Couleur'], ascending=[1])
    elif mode == "7":
        result = df.sort_values(['Origine'], ascending=[1])
    elif mode == "8":
        result = df.sort_values(['Matiere'], ascending=[1])
    elif mode == "9":
        result = df.loc[(df['Altitude'] >= 2400)]


    # Old test filter
    '''
    if mode == "1":
        result = df.loc[(df['Altitude'] >= 2400)]
    elif mode == "2":
        result = df.loc[(df['Altitude'] < 5)]
    elif mode == "3":
        result = df.loc[(df['Altitude'] >= 5) & (df['Altitude'] < 10)]
    elif mode == "4":
        result = df.loc[(df['Altitude'] >= 5) & (df['Altitude'] < 10)]
    elif mode == "5":
        result = df.sort_values(['Altitude'], ascending=[1])
    elif mode == "6":
        result = df.sort_values(['Couleur'], ascending=[1])
    elif mode == "7":
        result = df.sort_values(['Pays'], ascending=[1])
    '''

    # Display all results of the sequence selected
    object_result = np.array2string(result['Jour'].values, separator='-', prefix='', suffix='').replace(' ', '').replace('[', '').replace(']', '');
    # Print all objects with less columns
    print(result[['Jour', 'Annee', 'Mois', 'Pays', 'Altitude', 'Objet', 'Lieu', 'Contexte', 'Catégorie', 'Titre', 'Poids', 'Taille', 'Couleur', 'Matiere', 'Origine']])

    # Message send to OSC with the full sequence of objects
    print("Send an OSC message with the list {0}\n".format(object_result))
    clientSequence.send_message("/control/controler/filter/result", object_result)

    # Send each object of the sequence to processing
    if CONFIG_IS_SEND_TO_PROCESSING:
        for index, row in result.iterrows():
            print("Send OSC message /video/enveloppe/id %i on port %i", row["Jour"], CONFIG_IS_SEND_TO_PROCESSING)
            clientProcessing.send_message("/video/enveloppe/id", index+1)
            time.sleep(CONFIG_PROCESSING_MS_SLEEP_BETWEEN_IMAGE/1000)

    # Write the sequence in a CSV file
    result.to_csv('data-0-4_tab_header_cleaned' + mode + '.csv', sep='\t') 

    #   /video/list 12-345-12

# Start the server
print("Serving on {}".format(server.server_address))
server.serve_forever()