all:
	poetry run python destiny.py

install:
	poetry install

clean:
	rm -rf poetry.lock *.pyc

