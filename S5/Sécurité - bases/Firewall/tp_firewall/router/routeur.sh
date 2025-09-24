#!/bin/bash

# remise à 0 sans modifier la politique par défaut !
iptables -F
iptables -X
# politique par défaut
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Autoriser ICMP (ping) sur le routeur lui-même
iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT

# Autoriser ICMP en transit (client <-> DMZ)


