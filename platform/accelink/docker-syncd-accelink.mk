# docker image for accelink syncd

DOCKER_SYNCD_PLATFORM_CODE = accelink
include $(PLATFORM_PATH)/../template/docker-syncd-base.mk

$(DOCKER_SYNCD_BASE)_DEPENDS += $(SYNCD) \
                                $(SYNCD_DBG) \
                                $(LIBSWSSCOMMON_DBG) \
                                $(LIBLAIMETADATA_DBG) \
                                $(LIBLAIREDIS_DBG)
$(DOCKER_SYNCD_BASE)_DEPENDS += $(ACCELINK_LAI)

$(DOCKER_SYNCD_BASE)_DBG_DEPENDS += $(SYNCD_DBG) \
                                $(LIBSWSSCOMMON_DBG) \
                                $(LIBLAIMETADATA_DBG) \
                                $(LIBLAIREDIS_DBG)

$(DOCKER_SYNCD_BASE)_VERSION = 1.0.0
$(DOCKER_SYNCD_BASE)_PACKAGE_NAME = syncd
$(DOCKER_SYNCD_BASE)_MACHINE = accelink

$(DOCKER_SYNCD_BASE)_RUN_OPT += -v /host/warmboot:/var/warmboot
