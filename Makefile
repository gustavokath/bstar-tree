docker:
	docker build -t btree-python .
	docker run -it --rm --name btree-python-run btree-python
