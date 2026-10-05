To use this Onlinefom :
  - Install the dependencies : pip install -r requirements.txt
  - You need to run the server "server.py"
  - Install on your phone (android) : NetShare, it allows t share hotspot local network without using your 4g connection 
  - launch the hotspot from your phone
  - and have the students connect to it and connect your laptop that is hosting to your phone hotspot
  - url http://{pc-ip}:8000/attendance

Scanning instead of typing the url :
  - When the server starts it prints a QR code in the terminal, students can scan it directly to open the form
  - The QR code always points at the ip of the interface your laptop uses, so reconnect to the hotspot before starting the server
  - To show it on a projector or a bigger screen, open http://{pc-ip}:8000/qr

veryy important note:
  - Netshare may be limited on how many connection your phone can have so instruct others if they finish attendance to disconect from the network  
