run:
	dev_appserver.py -A transcation-example app.yaml

runclean:
	dev_appserver.py -A transcation-example app.yaml --clear_datastore

install: install-dev install-prod

install-prod:
	pip install -Ur requirements.txt -t vendor

install-dev:
	pip install -Ur requirements-dev.txt

clean:
	find . -name "*.py[co]" -delete
