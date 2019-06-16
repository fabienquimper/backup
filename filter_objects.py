import pandas as pd
import numpy as np
import argparse
import time
from array import array
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# Configuration
CONFIG_NETWORK_PORT_FOR_SEQUENCE = 8005
CONFIG_NETWORK_PORT_FOR_PROCESSING = 8003
CONFIG_IS_SEND_TO_PROCESSING = True
CONFIG_PROCESSING_MS_SLEEP_BETWEEN_IMAGE = 150

# Read CSV
df = pd.read_csv('data-0-4_tab_header_cleaned.csv', header=[0], sep='\t') 

print('All columns names:')
print(list(df.columns))
#'Jour', 'Annee', 'Mois', 'Jour.1', 'Depart', 'Arrivee', 'Pays', 'Km_jours', 'Km_cumule', 'Altitude', 'Lat_degres', 'Lat_minutes', 'Lat_decimale', 'Lat_radian', 'Long_degres', 'Long_minutes', 'Long_decimale', 'Long_radian', 'km_vol_oiseau', 'km_corde', 'km_segment', 'km_cumule', 'Unnamed: 22', 'Objet', 'Lieu', 'Contexte', 'Catégorie', 'Post', 'Jour xxx', 'Titre', 'Unnamed: 30', 'Poids', 'Taille', 'Couleur', 'Matiere', 'Origine', 'Unnamed: 36', 'Date', 'Coordonnees'

#print('Print all datas')
#print(df)

# Config filter
all_filter_value = []
all_filter_min_max = []

def add_value_filter(filterString):
    filterArray = filterString.split(" ")
    filterColumn = filterArray[0] #Exemple pays
    filterKey = filterArray[1] # Exemple France
    filterIsOn = filterArray[2] # Exemple 1

    # Update the filter
    isExisting = False;
    for index, filt in enumerate(all_filter_value):
        if (filt[0] == filterColumn and filt[1] == filterKey):
            isExisting = True
            all_filter_value[index][2] = filterIsOn 

    if not isExisting:
        all_filter_value.append(filterArray)

    print("All filter value:")
    print(all_filter_value)
def add_min_max_filter(filterString):
    filterArray = filterString.split(" ")
    filterColumn = filterArray[0] #Exemple altitude
    filterMin = int(filterArray[1]) # Exemple 23
    filterMax = int(filterArray[2]) # Exemple 2000

    # Update the filter
    isExisting = False;
    for index, filt in enumerate(all_filter_min_max):
        if (filt[0] == filterColumn):
            isExisting = True
            all_filter_min_max[index][1] = filterMin
            all_filter_min_max[index][2] = filterMax

    if not isExisting:
        all_filter_min_max.append((filterColumn, filterMin, filterMax))

    print("All filter min_max:")
    print(all_filter_min_max)
def get_data_from_filter():
    dfCopy = df.copy()
    # Add value filter
    for index, filt in enumerate(all_filter_value):
        if (filt[2] == "1"):
            dfCopy = dfCopy.loc[dfCopy[filt[0]] == filt[1]]

    # Add min-max filter
    for index, filt in enumerate(all_filter_min_max):
        dfCopy = dfCopy.loc[(dfCopy[filt[0]] >= int(filt[1])) & (dfCopy[filt[0]] <= int(filt[2]))]

    return dfCopy
def reset_filter():
    all_filter_value = []
    all_filter_min_max = []

    print("All filter min_max:")
    print(all_filter_min_max)

    print("All filter value:")
    print(all_filter_value)


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
    print("Filter value: col key isOn?:[{0}]".format(args))
    add_value_filter(args)
    objects_filtered()
def filter_reset(unused_addr, args):
    print("Filter reset.".format(args))
    reset_filter()
    objects_filtered()
def filter_min_max(unused_addr, args):
    print("Filter min-max: col min max:[{0}] ".format(args))
    add_min_max_filter(args)
    objects_filtered()
# Id mode has been received (from another OSC message)
dispatcher.map("/control/controler/sequence", print_objects)
dispatcher.map("/control/controler/filter/value", filter_value)
dispatcher.map("/control/controler/filter/reset", filter_reset)
dispatcher.map("/control/controler/filter/min-max", filter_min_max)
dispatcher.map("/control/controler/filter/result", print_list)
# Start the server
server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher) 
#### END OF OSC CONFIGURATION

def objects_filtered():
    dfFiltered = get_data_from_filter()
    #print(dfFiltered)
    output_objects(dfFiltered)

def output_objects(resultDf):
   # print(resultDf['Jour'])
    print(resultDf)

    #print(type(resultDf))
    #resultDf.to_csv('data-filtered.csv', sep='\t') 

    result = resultDf
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

    output_objects(result)

    # Write the sequence in a CSV file
    result.to_csv('data-0-4_tab_header_cleaned' + mode + '.csv', sep='\t') 

    #   /video/list 12-345-12

# Start the server
print("Serving on {}".format(server.server_address))
server.serve_forever()