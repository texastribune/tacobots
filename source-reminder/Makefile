deploy: install-deps
	zip -r deployment_package *
	aws lambda update-function-code \
	--region us-east-1 \
		--function-name sourceReminder \
		--zip-file fileb://deployment_package.zip
	rm deployment_package.zip

install-deps:
	pip3 install -t $$(pwd) -r $$(pwd)/requirements.txt


# docker commands
build-image:
	docker build -t source-reminder/lambda:local .

run-container: build-image
	docker run \
		--rm -it \
		-p 9000:8080 \
		-v $$(pwd)/credentials.json:/var/task/credentials.json \
		-v $$(pwd)/src/lambda_function.py:/var/task/lambda_function.py \
		--env-file=docker-env \
		--name source-reminder \
		source-reminder/lambda:local

test-container:
	curl -XPOST \
		"http://localhost:9000/2015-03-31/functions/function/invocations" \
		-d '{}'