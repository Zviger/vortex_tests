FROM vortex_toolchain:latest

# Installing and setup vortex
WORKDIR /vortexgpgpu/vortex

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