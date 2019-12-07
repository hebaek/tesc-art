/home/pi/data:
	mkdir /home/pi/data
	chown pi:pi /home/pi/data


install:	/home/pi/data
	install -o root -g root -m 755 -t /usr/local/src/ tesc-art.py
	install -o root -g root -m 644 -t /usr/local/src/ config.py
	install -o root -g root -m 644 -t /usr/local/src/ hardware.py
	install -o root -g root -m 644 -t /usr/local/src/ main.py
	install -o root -g root -m 644 -t /usr/local/src/ event.py

	install -o pi   -g pi   -m 644 -t /home/pi/data/  data/setup-example.txt
	install -o pi   -g pi   -m 644 -t /home/pi/data/  data/events-example.txt
	install -o pi   -g pi   -m 644 -t /home/pi/data/  data/tesc-art.conf

	install -o pi   -g pi   -m 755 -t /home/pi/		  tesc.sh
