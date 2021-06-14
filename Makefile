.PHONY: build
build: | submodule build_toolchain
	docker-compose build

.PHONY: build_toolchain
build_toolchain:
	docker build -f ./docker/toolchain.Dockerfile -t vortex_toolchain .

.PHONY: submodule
submodule:
	git submodule update --init --recursive

