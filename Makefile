all:
	poetry run python destiny.py $(BIRTH) $(SEX)

install:
	poetry install

clean:
	rm -rf poetry.lock *.pyc

