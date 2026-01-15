# sonic-yanggen.mk
# Platform makefile to generate SONiC YANG from annotation YANG and install CLI auto-generation service

SONIC_YANGGEN_VERSION = 1.0.0
export SONIC_YANGGEN_VERSION

SONIC_YANGGEN = sonic-yanggen_$(SONIC_YANGGEN_VERSION)_$(CONFIGURED_ARCH).deb
$(SONIC_YANGGEN)_SRC_PATH = $(PLATFORM_PATH)/sonic-yanggen
# Build libyang from source, no external dependencies
$(SONIC_YANGGEN)_BUILD_ENV = DEB_BUILD_OPTIONS=nocheck

SONIC_DPKG_DEBS += $(SONIC_YANGGEN)
