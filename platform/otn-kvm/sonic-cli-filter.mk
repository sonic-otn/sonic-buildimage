# sonic-cli-filter.mk
# Platform CLI command filter - removes unwanted switch commands

SONIC_CLI_FILTER_VERSION = 1.0.0
export SONIC_CLI_FILTER_VERSION

SONIC_CLI_FILTER = sonic-cli-filter_$(SONIC_CLI_FILTER_VERSION)_all.deb
$(SONIC_CLI_FILTER)_SRC_PATH = $(PLATFORM_PATH)/sonic-cli-filter
$(SONIC_CLI_FILTER)_DEPENDS += $(SONIC_UTILITIES_DATA)
$(SONIC_CLI_FILTER)_BUILD_ENV = DEB_BUILD_OPTIONS=nocheck

SONIC_DPKG_DEBS += $(SONIC_CLI_FILTER)
