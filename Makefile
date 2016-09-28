docker:
	docker build -t btree-python .
	docker run -it --rm -v data:/usr/src/app/data --name btree-python-run btree-python
