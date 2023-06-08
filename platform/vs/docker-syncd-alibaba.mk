# docker image for alibaba syncd

DOCKER_SYNCD_PLATFORM_CODE = alibaba
include $(PLATFORM_PATH)/../template/docker-syncd-base.mk

$(DOCKER_SYNCD_BASE)_DEPENDS += $(SYNCD_VS)

$(DOCKER_SYNCD_BASE)_DBG_DEPENDS += $(SYNCD_VS_DBG) \
                                $(LIBSWSSCOMMON_DBG) \
                                $(LIBLAIMETADATA_DBG) \
                                $(LIBLAIREDIS_DBG) \
                                $(LIBLAIVS_DBG)

$(DOCKER_SYNCD_BASE)_RUN_OPT += -v /host/warmboot:/var/warmboot
