from scapy.all import *
import smtplib


fromaddr = 'noohunufais.s@gmail.com'
toaddrs  = 'noohnufais13@gmail.com'
msg = 'Enter you message here'

username = 'noohunufais'
password = 'augb rxuj arcp wssu'

# Sending the mail  

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()


# def analyze_pcap(pcap_file):
 
#     packets = rdpcap(pcap_file)
    
  
#     print(packets[0]['SNMP']['SNMPtrapv2'].show())


# if __name__ == "__main__":

#     pcap_file = 'lab0.pcap'

#     analyze_pcap(pcap_file)
