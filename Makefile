all: app

requirements:
	cd documents/requirements && make

validation:
	cd documents/validation && make

thesis:
	cd thesis && make

app:

clean:
	cd documents/requirements && make clean
	cd thesis && make clean
