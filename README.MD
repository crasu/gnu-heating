# Decoder for eberle instat 868 heating control system #

### Setup gnuradio on Ubuntu ###
* Install gnuradio (Version >=3.7.x)
    
      apt install gnuradio
    
* Install gr-osmosdr blocks

      apt install
    
* Checkout this repo and submodules

      git clone --recurse-submodules <repo url>
    
* Build all gnuradio oot modules contained in the gr-xxx submodules

      cd gr-xxx
      mkdir build
      cd build/
      cmake ../
      make

### Setup mqtt and packet decoder ###

* Install a mqtt broker
   
      apt install mosquitto
   

* Update the ip in packet_decoder.py or in packet_decoder.grc
* Run the packet_decoder from cli via
    
      python packet_decoder.py
    
* Or via 

      gnuradio-companion packet_decoder.grc

* You should now be able to see mqtt packet containing the raw messages from the instat controllers
* You can pipe those messages to a text file

      nohup mosquitto_sub -t /gnuradio >> mosquitto_sub.log &

### Decoding the message to a human redable format

* To decode the mqtt message content run the parser on the logfile content

      tail  -f mosquitto_sub.log|python3 parser/parser.py 
