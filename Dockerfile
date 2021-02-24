FROM ubuntu:18.04

# Installing required libs
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN apt-get update -y

RUN apt-add-repository -y "ppa:ubuntu-toolchain-r/test"

RUN apt-get install -yq --no-install-suggests --no-install-recommends \
   build-essential \
   git valgrind \
   binutils build-essential libtool texinfo \
   gzip zip unzip patchutils curl git \
   make cmake ninja-build automake bison flex gperf \
   grep sed gawk python bc \
   zlib1g-dev libexpat1-dev libmpc-dev \
   libglib2.0-dev libfdt-dev libpixman-1-dev wget


# Installing and setup toolchain
WORKDIR vortexgpgpu/vortex

COPY ./toolchain_install.sh  /vortexgpgpu/vortex/ci/toolchain_install.sh

ENV CXX=${CXX:-g++}
ENV CXX_FOR_BUILD=${CXX_FOR_BUILD:-g++}
ENV CC=${CC:-gcc}
ENV CC_FOR_BUILD=${CC_FOR_BUILD:-gcc}
RUN gcc --version

RUN ci/toolchain_install.sh -all

ENV RISCV_TOOLCHAIN_PATH=/opt/riscv-gnu-toolchain
ENV VERILATOR_ROOT=/opt/verilator
ENV PATH=$VERILATOR_ROOT/bin:$PATH


# Installing and setup vortex

# Cloning vortex from vortex github
#RUN git clone --depth=50 --branch=master https://github.com/vortexgpgpu/vortex.git vortexgpgpu/vortex
#RUN git submodule update --init --recursive

# Cloning vortex from local ./vortex directory
# If u want to change something in code base, u can run previos 2 commands in root/vortex dir
COPY ./vortex /vortexgpgpu/vortex

RUN make

# Run commands from test.sh
COPY ./test.sh  /vortexgpgpu/vortex/test.sh
RUN chmod +x ./test.sh
RUN ./test.sh



# Tests from vortex ci
#RUN ./ci/test_runtime.sh
#RUN ./ci/test_riscv_isa.sh
#RUN ./ci/test_opencl.sh
#RUN ./ci/test_driver.sh
#RUN ./ci/travis_run.py ./ci/blackbox.sh --driver=vlsim --cores=1 --perf --app=demo --args="-n1"
#RUN ./ci/travis_run.py ./ci/blackbox.sh --driver=vlsim --cores=1 --debug --app=demo --args="-n1"
#RUN ./ci/travis_run.py ./ci/blackbox.sh --driver=vlsim --cores=1 --scope --app=demo --args="-n1"
#RUN /ci/travis_run.py ./ci/blackbox.sh --driver=rtlsim --cores=2 --clusters=2 --app=demo --args="-n1"
#RUN ./ci/travis_run.py ./ci/blackbox.sh --driver=rtlsim --cores=2 --l2cache --app=demo --args="-n1"
#RUN ./ci/travis_run.py ./ci/blackbox.sh --driver=rtlsim --cores=2 --clusters=2 --l2cache --l3cache --app=demo --args="-n1"
#RUN lcov --directory . --capture --output-file coverage.info
#RUN lcov --list coverage.info
#RUN bash <(curl -s https://codecov.io/bash)