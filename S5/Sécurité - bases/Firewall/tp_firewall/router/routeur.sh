#!/bin/bash

# remise à 0 sans modifier la politique par défaut !
iptables -F
iptables -X
# politique par défaut
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Autoriser ICMP (ping) sur le routeur lui-même
iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT

#SSH depuis le client vers le routeur
# (client = 192.168.1.1 / routeur = 192.168.1.254)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

iptables -S
