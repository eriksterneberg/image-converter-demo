.PHONY: staticd testd pycodestyle test clean-pyc

pycodestyle: 
	@ echo "Running code style test..."
	@ docker-compose run web pycodestyle ./

test:
	@ echo "Running tests..."
	@ docker-compose run web python -m unittest discover tests/ "test_*.py"

clean-pyc:
	@ echo "Cleaning .pyc files"
	@ find . -name \*.pyc -delete 2>/dev/null

staticd:
	@ docker-compose down --remove-orphans 2>/dev/null 1>&2
	@ docker-compose up --build -d web 2>/dev/null 1>&2
	@ make clean-pyc
	@ make pycodestyle
	@ docker-compose down --remove-orphans 2>/dev/null 1>&2

testd:
	@ docker-compose down --remove-orphans 2>/dev/null 1>&2
	@ docker-compose up --build -d web 2>/dev/null 1>&2
	@ make clean-pyc
	@ make test
	@ docker-compose down --remove-orphans 2>/dev/null 1>&2