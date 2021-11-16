TEST_IMAGE_PATH = ./tests/test_image.jpg
TEST_CONFIG_PATH = ./tests/test_config.json
PROCESSED_DIR = ./processed
PROCESSED_NAME_BASE = test_image_processed.jpg
TEST_TITLE = title
TEST_TEXT = text


build:
	python setup.py sdist
	python setup.py bdist_wheel


build_docs:
	pip install sphinx sphinx_rtd_theme
	sphinx-apidoc -f -o docs_src protreim
	sphinx-build ./docs_src ./docs
	touch docs/.nojekyll


testall: \
	mypy \
	unittest \
	clitest \
	guitest


mypy: 
	mypy --strict --ignore-missing-imports protreim tests


unittest:
	python -m unittest tests


clitest:
	protreim --version
	protreim -f $(TEST_IMAGE_PATH) -o $(PROCESSED_DIR)/$(PROCESSED_NAME_BASE) --log-level debug --config $(TEST_CONFIG_PATH)
	protreim -f $(TEST_IMAGE_PATH) -o $(PROCESSED_DIR)/title.$(PROCESSED_NAME_BASE) --log-level debug --title $(TEST_TITLE) --config $(TEST_CONFIG_PATH)
	protreim -f $(TEST_IMAGE_PATH) -o $(PROCESSED_DIR)/text.$(PROCESSED_NAME_BASE) --log-level debug --text  $(TEST_TEXT) --config $(TEST_CONFIG_PATH)


guitest:

	





