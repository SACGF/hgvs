PACKAGE_NAME=pyhgvs

default: package

.PHONY: clean lint test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf __pycache__/
	rm -f MANIFEST
	rm -f $(TEST_OUTPUT)
	find $(PACKAGE_NAME) -type f -name '*.pyc' -delete

lint:
	flake8 --jobs=auto $(PACKAGE_NAME)/ $(SCRIPTS)

package:
	python3 -m build
