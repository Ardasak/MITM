import scapy.all as scapy
import optparse



def get_user_input():
    parse_obj=optparse.OptionParser()
    parse_obj.add_option("-i","--ipaddress",dest="ip_address",help="Enter IP Address")

    (input,arguments)=parse_obj.parse_args()

    if not input.ip_address:
        print("Enter IP Address")

    return input

def scan_network(ip):
    arp_request_packet=scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined = broadcast_packet/arp_request_packet
    (answered_list,unanswered_list)=scapy.srp(combined,timeout = 1)
    answered_list.summary()

user_ip=get_user_input()
scan_network(user_ip.ip_address)
