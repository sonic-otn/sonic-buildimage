# lairedis package

LIBLAIREDIS = liblairedis_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBLAIREDIS)_DPKG_TARGET = binary-lairedis
$(LIBLAIREDIS)_SRC_PATH = $(SRC_PATH)/sonic-lairedis
$(LIBLAIREDIS)_DEPENDS += $(LIBSWSSCOMMON_DEV)
$(LIBLAIREDIS)_RDEPENDS += $(LIBSWSSCOMMON)
$(LIBLAIREDIS)_DEB_BUILD_OPTIONS = nocheck
SONIC_DPKG_DEBS += $(LIBLAIREDIS)

LIBLAIREDIS_DEV = liblairedis-dev_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIREDIS_DEV)))

LIBLAIVS = liblaivs_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIVS)))

LIBLAIVS_DEV = liblaivs-dev_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIVS_DEV)))
$(LIBLAIVS_DEV)_DEPENDS += $(LIBLAIVS)

LIBLAIMETADATA = liblaimetadata_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIMETADATA)))

LIBLAIMETADATA_DEV = liblaimetadata-dev_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBLAIMETADATA_DEV)_DEPENDS += $(LIBLAIMETADATA)
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIMETADATA_DEV)))

LIBLAIREDIS_DBG = liblairedis-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBLAIREDIS_DBG)_DEPENDS += $(LIBLAIREDIS)
$(LIBLAIREDIS_DBG)_RDEPENDS += $(LIBLAIREDIS)
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIREDIS_DBG)))

LIBLAIVS_DBG = liblaivs-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBLAIVS_DBG)_DEPENDS += $(LIBLAIVS)
$(LIBLAIVS_DBG)_RDEPENDS += $(LIBLAIVS)
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIVS_DBG)))

LIBLAIMETADATA_DBG = liblaimetadata-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBLAIMETADATA_DBG)_DEPENDS += $(LIBLAIMETADATA)
$(LIBLAIMETADATA_DBG)_RDEPENDS += $(LIBLAIMETADATA)
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(LIBLAIMETADATA_DBG)))

# The .c, .cpp, .h & .hpp files under src/{$DBG_SRC_ARCHIVE list}
# are archived into debug one image to facilitate debugging.
#
DBG_SRC_ARCHIVE += sonic-lairedis
