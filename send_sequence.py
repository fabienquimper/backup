"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=8005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  selectionMode = "1"
  while (selectionMode != "exit"):
    selectionMode = input("Type a mode (1, 2, 3, ... or 'exit' to quit: ")
    if selectionMode == "exit":
      exit(0)
    elif selectionMode.isdigit():
      print("Send an OSC message with the mode {0}\n".format(selectionMode))
      client.send_message("/control/controler/sequence", selectionMode)
    else:
      print ("'{0}' is not a digit or 'exit' string".format(selectionMode))
      exit(0);