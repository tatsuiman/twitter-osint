#!/bin/bash
# install ELK
wget https://artifacts.elastic.co/downloads/kibana/kibana-5.5.2-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.2.deb
wget https://artifacts.elastic.co/downloads/logstash/logstash-5.5.2.deb
sudo dpkg -i *.deb

# install logstash plugins
sudo /usr/share/logstash/bin/logstash-plugin install logstash-input-twitter

# register and start service
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl enable kibana.service
sudo systemctl start kibana.service
sudo systemctl enable logstash.service
sudo systemctl start logstash.service

# wait elasticsearch
while ! nc -z localhost 9200; do   
  sleep 0.1
done
./load.sh
