#!/bin/sh
echo "Flushing iptables rules..."
sleep 1
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPTED
iptables -P FORWARD ACCEPTED
iptables -P OUTPUT ACCEPTED

echo "Setting iptables rules..."

## DNS ##
#From internet to external DNS server, DNS queries accepted
iptables -A FORWARD -i eth0 -p tcp -m tcp -d 10.19.1.12 --dport 53 -j ACCEPT
#From DMZ to internal DNS server, DNS queries accepted
iptables -A FORWARD -i eth1 -p tcp -m tcp -d 10.19.1.142 --dport 53 -j ACCEPT
#External DNS server can send out query respond
iptables -A FORWARD  -p tcp -m tcp -s 10.19.1.12 --sport 53 -j ACCEPT
#External DNS server can send out DNS query to host on internet
iptables -A FORWARD  -p tcp -m tcp -s 10.19.1.12 --sport 53 -o eth0 --dport 53 -j ACCEPT

## MAIL ##
#Hosts on internet can connect to SMTP on external mail server
iptables -A FORWARD -i eth0 -p tcp -m tcp -d 10.19.1.11 --dport 25 -j ACCEPT
#External mail server can connect to SMTP on internal mail server
iptables -A FORWARD -s 10.19.1.11 -p tcp -m tcp -d 10.19.1.141 --dport 25 -j ACCEPT
#Internal mail server can connect to SMTP on mail servers on internet
iptables -A FORWARD -s 10.19.1.141 -p tcp -m tcp -o eth0 --dport 25 -j ACCEPT
#Host on LAN can't send SMTP on host on internet or DMZ
iptables -A FORWARD -o eth2 -p tcp -m tcp --dport 25 -j DROP

## WEB ## 
# Internet hosts can connect using HTTP to external web server
iptables -A FORWARD -i eth0 -p tcp -m tcp --sport 80  -d 10.19.1.10 -j ACCEPT

## FIREWALL ##
#Firewall must communicate with itself
iptables -A INPUT -s 10.19.0.1 -j ACCEPT 
iptables -A OUTPUT -d 10.19.0.1 -j ACCEPT
#Firewall accept rip traffic from internet
iptables -A INPUT -i eth0 -p udp -m udp --sport 520 -d 10.19.0.1 -j ACCEPT
#Firewall accepts ssh connections from LAN
iptables -A INPUT -i eth2 -p tcp -m tcp -d 10.19.0.1 --dport 22  -j ACCEPT
#Firewall must not accept any traffic from LAN,DMZ or Internet
iptables -A INPUT -d 10.19.0.1 -j DROP

## OTHER ## TODO: Ask L.A how to read this command correcly and should this be above firewall rule since we disguise the ip?
#Firewall implement source NAT for LAN hosts in 192.168.12.0/24
iptables -t nat -A POSTROUTING -s 10.19.1.129 -d 192.168.12.0/24  -j SNAT --to-source 10.19.0.1

#Ipsec connections permitted from internet to LAN
#Port 500, allows ISAKMP traffic, ip portocol id 51 allows AH traffic 
#ip portocol id 50 allows ESP traffic. drop all other traffic 
iptables -A FORWARD -i eth0 -p udp -m udp -o eth2 --dport 500 -j ACCEPT
iptables -A FORWARD -i eth0 -p tcp -m tcp -o eth2 --dport 51 -j ACCEPT
iptables -A FORWARD -i eth0 -p tcp -m tcp -o eth2 --dport 50 -j ACCEPT

#Keeping the good ICMP types destination unreachable/source quench. Drop the rest
iptables -A FORWARD -i eth0 -p icmp --icmp-type 3 -o eth2 -j ACCEPT
iptables -A FORWARD -i eth0 -p icmp --icmp-type 4 -o eth2 -j ACCEPT
iptables -A FORWARD -i eth0 -p icmp -o eth2 -j DROP

## GENERAL ##
#Deny new connections from internet 
iptables -A FORWARD -i eth0 -m state --state NEW -j DROP 
#Deny new connections from DMZ
iptables -A FORWARD -i eth1 -m state --state NEW -j DROP 
#New connections from LAN is allowed
iptables -A FORWARD -i eth2 -m state --state NEW -j ACCEPT 

# TODO: should we drop the rest of the connections?
#iptables -A FORWARD -j DROP

echo "Setting iptables rules... done"
