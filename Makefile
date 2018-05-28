build-app:
	docker build --file=Dockerfile -t lesara_test/bash:dev .

server-start: build-app
	docker run --rm -it \
	    -v ${PWD}/output_files:/opt/lesara_test/output_files \
	    -p 8000:5000  \
	    --name lesara-test-app \
	    lesara_test/bash:dev \
	    ./run.sh

unittest: build-app
	docker run --rm -i \
	--name lesara-unittests \
	lesara_test/bash:dev \
	python3 -m unittest
