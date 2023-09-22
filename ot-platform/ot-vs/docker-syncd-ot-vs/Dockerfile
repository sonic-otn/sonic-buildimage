FROM docker-config-engine-buster

ARG docker_container_name
# Auto-Generated for buildinfo
ARG SONIC_VERSION_CACHE
ARG SONIC_VERSION_CONTROL_COMPONENTS
COPY ["buildinfo", "/usr/local/share/buildinfo"]
COPY vcache/ /sonic/target/vcache/docker-syncd-ot-vs
RUN dpkg -i /usr/local/share/buildinfo/sonic-build-hooks_1.0_all.deb
ENV IMAGENAME=docker-syncd-ot-vs
ENV DISTRO=buster
RUN pre_run_buildinfo docker-syncd-ot-vs

RUN [ -f /etc/rsyslog.conf ] && sed -ri "s/%syslogtag%/$docker_container_name#%syslogtag%/;" /etc/rsyslog.conf

## Make apt-get non-interactive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -f -y iproute2 libcap2-bin gdb

COPY \
debs/libnl-3-200_3.5.0-1_amd64.deb debs/libnl-route-3-200_3.5.0-1_amd64.deb debs/libnl-genl-3-200_3.5.0-1_amd64.deb debs/libnl-nf-3-200_3.5.0-1_amd64.deb debs/libnl-cli-3-200_3.5.0-1_amd64.deb debs/libyang_1.0.73_amd64.deb debs/libswsscommon_1.0.0_amd64.deb debs/libotairedis_1.0.0_amd64.deb debs/libotaimetadata_1.0.0_amd64.deb debs/libotaivs_1.0.0_amd64.deb debs/syncd-ot-vs_1.0.0_amd64.deb debs/

RUN dpkg -i \
debs/libnl-3-200_3.5.0-1_amd64.deb debs/libnl-route-3-200_3.5.0-1_amd64.deb debs/libnl-genl-3-200_3.5.0-1_amd64.deb debs/libnl-nf-3-200_3.5.0-1_amd64.deb debs/libnl-cli-3-200_3.5.0-1_amd64.deb debs/libyang_1.0.73_amd64.deb debs/libswsscommon_1.0.0_amd64.deb debs/libotairedis_1.0.0_amd64.deb debs/libotaimetadata_1.0.0_amd64.deb debs/libotaivs_1.0.0_amd64.deb debs/syncd-ot-vs_1.0.0_amd64.deb 

COPY ["start.sh", "/usr/bin/"]

COPY ["supervisord.conf", "/etc/supervisor/conf.d/"]
COPY ["files/supervisor-proc-exit-listener", "/usr/bin"]
COPY ["critical_processes", "/etc/supervisor/"]

## Clean up
RUN apt-get clean -y; apt-get autoclean -y; apt-get autoremove -y
RUN rm -rf /debs

ENTRYPOINT ["/usr/local/bin/supervisord"]

RUN post_run_buildinfo docker-syncd-ot-vs 

RUN post_run_cleanup docker-syncd-ot-vs 
