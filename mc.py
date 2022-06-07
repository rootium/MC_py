from os import system
from mcstatus import JavaServer
from threading import Thread
from pymongo import MongoClient

def mc(ip):
    try:
        mc = JavaServer(ip).status().raw
        version = mc["version"]["name"]
        online = mc["players"]["online"]
        if online != 0:
            players = mc["players"]["sample"]
            text = {'ip':ip,'version':version,'online':online,'players':players}
        else:
            text = {'ip':ip,'version':version,'online':online}
        mc_ips.append(text)
    except:
        pass

client = MongoClient('mongodb+srv://gigachadd:asdfwer123@cluster0.vlurn.mongodb.net/?retryWrites=true&w=majority').mc.mc_ip

def main():
  system("masscan 0.0.0.0/0 -p25565 -oX scan.xml --max-rate 100000 --exclude 255.255.255.255")

  txt = open("scan.xml", "r")
  scan = txt.read().split("\n")
  txt.close()

  c = 5
  port_ips = []
  while 1:
    try:
      i = scan[c].split('"')[3]
      c += 1
      port_ips.append(i)
    except:
      break

  T = 1000
  c = 0
  f = 1
  mc_ips = []
  while f == 1:
    threads = []
    for i in range(T):
      try:
        i = Thread(target = mc, args = (port_ips[c],))
        i.start()
        threads.append(i)
        c += 1
      except:
        f = 0
        break
    for i in threads:
      i.join()

  system("rm -d scan.xml")
  client.drop()
  client.insert_many(mc_ips)

while 1:
  main()
