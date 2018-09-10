all: app

requirements:
	cd documents/requirements && make

thesis:
	cd thesis && make

app:

clean:
	cd documents/requirements && make clean
