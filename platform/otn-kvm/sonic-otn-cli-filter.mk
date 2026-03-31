# sonic-otn-cli-filter.mk
# Platform CLI command filter for OCS/OTN - removes unwanted switch commands

SONIC_OTN_CLI_FILTER_VERSION = 1.0.0
export SONIC_OTN_CLI_FILTER_VERSION

SONIC_OTN_CLI_FILTER = sonic-otn-cli-filter_$(SONIC_OTN_CLI_FILTER_VERSION)_all.deb
$(SONIC_OTN_CLI_FILTER)_SRC_PATH = $(PLATFORM_PATH)/sonic-otn-cli-filter
$(SONIC_OTN_CLI_FILTER)_DEPENDS += $(SONIC_UTILITIES_DATA)
$(SONIC_OTN_CLI_FILTER)_BUILD_ENV = DEB_BUILD_OPTIONS=nocheck

SONIC_DPKG_DEBS += $(SONIC_OTN_CLI_FILTER)
