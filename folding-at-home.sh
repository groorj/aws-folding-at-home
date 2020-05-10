#!/bin/bash

# user config
FAH_USER="GustavoAguiar"
FAH_TEAM="238681" # Orange Nation
FAH_PASS=""
YOUR_IP_ADDRESS=""

# https://stats.foldingathome.org/donor/${FAH_USER}
# https://stats.foldingathome.org/team/${FAH_TEAM}

# update
yum update -y

# download 
wget "https://download.foldingathome.org/releases/public/release/fahcontrol/centos-6.7-64bit/v7.5/fahcontrol-7.5.1-1.noarch.rpm"
wget "https://download.foldingathome.org/releases/public/release/fahclient/centos-6.7-64bit/v7.5/fahclient-7.5.1-1.x86_64.rpm"

# install
yum install pygtk2 -y
yum install htop -y
rpm -i --nodeps fahcontrol-7.5.1-1.noarch.rpm
rpm -i --nodeps fahclient-7.5.1-1.x86_64.rpm

# config
cp -pd /etc/fahclient/config.xml /etc/fahclient/config.xml.orig
cat /etc/fahclient/config.xml <<EOF
<config>
 <! — Client Control →
 <fold-anon v=’true’/>

<! — Folding Slot Configuration →
 **<gpu v=’true’/>**

<! — Slot Control →
 <power v=’full’/>

<! — User Information →
 <user v=’JulienS’/>

<! — Folding Slots →
 <slot id=’0' type=’CPU’/>
 **<slot id=’1' type=’GPU’/>**
</config>
EOF

# start
/etc/init.d/FAHClient stop
/etc/init.d/FAHClient start

# End;
