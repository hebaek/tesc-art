$(home)/data:
	mkdir $(home)/data
	chown $(user):$(user) $(home)/data


install:	$(home)/data
	install -o root -g root -m 755 -t /usr/local/src/ tesc-art.py
	install -o root -g root -m 644 -t /usr/local/src/ config.py
	install -o root -g root -m 644 -t /usr/local/src/ hardware.py
	install -o root -g root -m 644 -t /usr/local/src/ file.py
	install -o root -g root -m 644 -t /usr/local/src/ main.py
	install -o root -g root -m 644 -t /usr/local/src/ event.py
	install -o root -g root -m 644 -t /usr/local/src/ variables.py

	install -o $(user) -g $(user) -m 644 -t $(home)/data/ data/hwsetup-example.txt
	install -o $(user) -g $(user) -m 644 -t $(home)/data/ data/events-example.txt
	install -o $(user) -g $(user) -m 644 -t $(home)/data/ data/tesc-art.conf

	install -o $(user) -g $(user) -m 755 -t $(home)       tesc.sh
