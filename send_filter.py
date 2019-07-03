"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Configuration
CONFIG_NETWORK_PORT_FOR_SEQUENCE = 8005

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=CONFIG_NETWORK_PORT_FOR_SEQUENCE,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  selectionMode = "1"
  while (selectionMode != "exit"):
    selectionMode = input("Type a filter (value / min-max / reset ... or 'exit' to quit: ")
    if selectionMode == "value":
      columnName = input("Type a column value (pays, id_couleur, id_materiel, origine): ")
      keyValue = input("Type a key value (pour le pays cela peut être France, Moroco, .....): ")
      onOffValue = input("Type 1 (ON) or 0 (OFF): ")
      client.send_message("/control/controler/filter/value", columnName + " " + keyValue + " " + onOffValue)
    elif selectionMode == "min-max":
      columnName = input("Type a column value (alti, kms, 'Poids (g)', taille): ")
      minValue = input("Type min value (23): ")
      maxValue = input("Type max value (2300): ")
      client.send_message("/control/controler/filter/min-max", columnName + " " + minValue + " " + maxValue)
    elif selectionMode == "reset":
      client.send_message("/control/controler/filter/reset", "1")
    elif selectionMode.isdigit():
      print("Send an OSC message with the mode {0}\n".format(selectionMode))
      client.send_message("/control/controler/sequence", selectionMode)
    else:
      print ("'{0}' is not a digit or 'exit' string".format(selectionMode))
      exit(0);