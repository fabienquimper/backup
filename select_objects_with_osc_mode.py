import pandas as pd
import numpy as np
import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# Configuration
PORT_TO_RECEIVE_MODE = 8005

######## Configure the server / client
# Set-up OSC server
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
parser.add_argument("--port", type=int, default=PORT_TO_RECEIVE_MODE, help="The port to listen on")
args = parser.parse_args()
# OSC client
client = udp_client.SimpleUDPClient(args.ip, args.port)
# Reception OSC message (mode)
def print_objects(unused_addr, args):
    print("Mode received: [{0}]".format(args[0]))
    objects_selector(args[0])
# Reception OSC message (list)
def print_list(unused_addr, args):
    print("List received: [{0}]".format(args))
dispatcher = dispatcher.Dispatcher()
# Id mode has been received (from another OSC message)
dispatcher.map("/video/mode", print_objects)
dispatcher.map("/video/list", print_list)
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

    object_result = np.array2string(result['Jour'].values, separator='-', prefix='', suffix='').replace(' ', '').replace('[', '').replace(']', '');
    # Print all objects with less columns
    print(result[['Jour', 'Annee', 'Mois', 'Pays', 'Altitude', 'Objet', 'Lieu', 'Contexte', 'Catégorie', 'Titre', 'Poids', 'Taille', 'Couleur', 'Matiere', 'Origine']])

    # Message send to OSC
    print("Send an OSC message with the list {0}\n".format(object_result))
    client.send_message("/video/list", object_result)

# Start the server
print("Serving on {}".format(server.server_address))
server.serve_forever()