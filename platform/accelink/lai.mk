ACCELINK_LAI=liblaiaccelink.deb
ACCELINK_LAI_DEV=liblaiaccelink-dev.deb
$(ACCELINK_LAI)_PATH=/sonic/platform/accelink/
$(ACCELINK_LAI_DEV)_PATH=/sonic/platform/accelink/

SONIC_COPY_DEBS += $(ACCELINK_LAI) $(ACCELINK_LAI_DEV)

$(eval $(call add_conflict_package,$(ACCELINK_LAI_DEV),$(LIBLAIVS_DEV)))
