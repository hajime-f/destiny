all:
	poetry run python destiny2.py

install:
	poetry install

clean:
	rm -rf poetry.lock *.pyc

