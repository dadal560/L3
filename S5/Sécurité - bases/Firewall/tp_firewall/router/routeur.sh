# Remise à zéro
iptables -F
iptables -X
iptables -t nat -F
iptables -t mangle -F

# Politiques par défaut
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# ICMP (ping)
iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT

# SSH autorisé seulement depuis le client
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.1 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -d 192.168.1.1 -j ACCEPT

# HTTP client -> DMZ
iptables -A FORWARD -p tcp --dport 80 -s 192.168.1.0/24 -d 10.192.10.10 -j ACCEPT
iptables -A FORWARD -p tcp --sport 80 -s 10.192.10.10 -d 192.168.1.0/24 -j ACCEPT

# DNS client -> DMZ
iptables -A FORWARD -p udp --dport 53 -s 192.168.1.0/24 -d 10.192.10.10 -j ACCEPT
iptables -A FORWARD -p udp --sport 53 -s 10.192.10.10 -d 192.168.1.0/24 -j ACCEPT

