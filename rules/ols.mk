# OLS (Optical Line System) package

SONIC_OLS_VERSION = 1.0.0-0
SONIC_OLS_PKG_NAME = ols

SONIC_OLS = sonic-$(SONIC_OLS_PKG_NAME)_$(SONIC_OLS_VERSION)_$(CONFIGURED_ARCH).deb
$(SONIC_OLS)_SRC_PATH = $(SRC_PATH)/sonic-ols
$(SONIC_OLS)_DEPENDS += $(LIBSWSSCOMMON) $(LIBSWSSCOMMON_DEV)

SONIC_DPKG_DEBS += $(SONIC_OLS)

SONIC_OLS_DBG = sonic-$(SONIC_OLS_PKG_NAME)-dbgsym_$(SONIC_OLS_VERSION)_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(SONIC_OLS),$(SONIC_OLS_DBG)))

# The .c, .cpp, .h & .hpp files under src/{$DBG_SRC_ARCHIVE list}
# are archived into debug one image to facilitate debugging.
#
DBG_SRC_ARCHIVE += sonic-ols
