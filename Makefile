CURRENT_PATH=$(shell pwd)
SETUP_FILE=$(CURRENT_PATH)/setup.py

.PHONY:build

build:
	python3 setup.py sdist bdist_wheel

deps:
	pip3 install -r $(CURRENT_PATH)/requirements.txt 
	pip3 install twine

publish-test:
	twine upload --repository-url https://test.pypi.org/legacy/ $(CURRENT_PATH)/dist/*

publish-release:
	twine upload $(CURRENT_PATH)/dist/*

check:
	python3 $(SETUP_FILE) check

generate-requrements:
	pipreqs $(CURRENT_PATH) --force
