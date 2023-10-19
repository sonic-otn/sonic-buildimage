# otss package

OTSS = otss_1.0.0_$(CONFIGURED_ARCH).deb
$(OTSS)_SRC_PATH = $(SRC_PATH)/sonic-otss
$(OTSS)_DEPENDS += $(LIBOTAIREDIS_DEV) $(LIBOTAIMETADATA_DEV) $(LIBTEAM_DEV) \
    $(LIBTEAMDCTL) $(LIBTEAM_UTILS) $(LIBSWSSCOMMON_DEV) \
    $(LIBOTAIVS) $(LIBOTAIVS_DEV) 
$(OTSS)_UNINSTALLS = $(LIBOTAIVS_DEV)

$(OTSS)_RDEPENDS += $(LIBOTAIREDIS) $(LIBOTAIMETADATA) $(LIBTEAM) \
    $(LIBTEAMDCTL) $(LIBSWSSCOMMON) $(PYTHON3_SWSSCOMMON)
SONIC_DPKG_DEBS += $(OTSS)

OTSS_DBG = otss-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(OTSS_DBG)_DEPENDS += $(OTSS)
$(OTSS_DBG)_RDEPENDS += $(OTSS)
$(eval $(call add_derived_package,$(OTSS),$(OTSS_DBG)))

# The .c, .cpp, .h & .hpp files under src/{$DBG_SRC_ARCHIVE list}
# are archived into debug one image to facilitate debugging.
#
DBG_SRC_ARCHIVE += sonic-otss

