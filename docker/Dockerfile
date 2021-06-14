FROM vortex_toolchain:latest

# Installing and setup vortex
WORKDIR /vortexgpgpu/vortex

COPY ./vortex /vortexgpgpu/vortex

RUN make
COPY ./sleep.sh .
RUN chmod +x ./sleep.sh
