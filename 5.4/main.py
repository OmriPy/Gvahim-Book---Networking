from scapy.all import *

#1
def ip_to_google():
    ip = IP(dst="www.google.com")
    ip.show()
    return ip

#2
def send_ip(ip):
    send(ip)

#3
def print_names(pkt):
    print(pkt.summary())

def facebook_summary():
    sniff(count=5, filter="dst www.facebook.com", prn=print_names)


def main():
    ip = ip_to_google()
    send_ip(ip)
    facebook_summary()

if __name__ == '__main__':
    main()
