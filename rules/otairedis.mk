# otairedis package

LIBOTAIREDIS = libotairedis_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBOTAIREDIS)_DPKG_TARGET = binary-otairedis
$(LIBOTAIREDIS)_SRC_PATH = $(SRC_PATH)/sonic-otairedis
$(LIBOTAIREDIS)_DEPENDS += $(LIBSWSSCOMMON_DEV)
$(LIBOTAIREDIS)_RDEPENDS += $(LIBSWSSCOMMON)
$(LIBOTAIREDIS)_DEB_BUILD_OPTIONS = nocheck
SONIC_DPKG_DEBS += $(LIBOTAIREDIS)

LIBOTAIREDIS_DEV = libotairedis-dev_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIREDIS_DEV)))

LIBOTAIVS = libotaivs_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIVS)))

LIBOTAIVS_DEV = libotaivs-dev_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIVS_DEV)))
$(LIBOTAIVS_DEV)_DEPENDS += $(LIBOTAIVS)

LIBOTAIMETADATA = libotaimetadata_1.0.0_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIMETADATA)))

LIBOTAIMETADATA_DEV = libotaimetadata-dev_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBOTAIMETADATA_DEV)_DEPENDS += $(LIBOTAIMETADATA)
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIMETADATA_DEV)))

LIBOTAIREDIS_DBG = libotairedis-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBOTAIREDIS_DBG)_DEPENDS += $(LIBOTAIREDIS)
$(LIBOTAIREDIS_DBG)_RDEPENDS += $(LIBOTAIREDIS)
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIREDIS_DBG)))

LIBOTAIVS_DBG = libotaivs-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBOTAIVS_DBG)_DEPENDS += $(LIBOTAIVS)
$(LIBOTAIVS_DBG)_RDEPENDS += $(LIBOTAIVS)
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIVS_DBG)))

LIBOTAIMETADATA_DBG = libotaimetadata-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(LIBOTAIMETADATA_DBG)_DEPENDS += $(LIBOTAIMETADATA)
$(LIBOTAIMETADATA_DBG)_RDEPENDS += $(LIBOTAIMETADATA)
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(LIBOTAIMETADATA_DBG)))

# The .c, .cpp, .h & .hpp files under src/{$DBG_SRC_ARCHIVE list}
# are archived into debug one image to facilitate debugging.
#
DBG_SRC_ARCHIVE += sonic-otairedis
