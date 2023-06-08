include $(PLATFORM_PATH)/lai.mk
include $(PLATFORM_PATH)/sonic-version.mk
include $(PLATFORM_PATH)/docker-syncd-accelink.mk
include $(PLATFORM_PATH)/obx1100-factory-config.mk
include $(PLATFORM_PATH)/one-image.mk

SONIC_ALL += $(SONIC_ONE_IMAGE)

$(SYNCD)_DEPENDS += $(ACCELINK_LAI) $(ACCELINK_LAI_DEV)
$(SYNCD)_RDEPENDS += $(ACCELINK_LAI_DEV) $(ACCELINK_LAI)

