include $(PLATFORM_PATH)/otn-libs-release.mk
include $(PLATFORM_PATH)/sai.mk
include $(PLATFORM_PATH)/docker-syncd-otn-kvm.mk
include $(PLATFORM_PATH)/platform-modules-otn-kvm.mk
include $(PLATFORM_PATH)/sonic-version.mk
include $(PLATFORM_PATH)/sonic-cli-filter.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/onie.mk
include $(PLATFORM_PATH)/kvm-image.mk
include $(PLATFORM_PATH)/raw-image.mk

SONIC_ALL += $(SONIC_ONE_IMAGE) $(SONIC_KVM_IMAGE) $(SONIC_RAW_IMAGE)

# Inject otn-kvm sai into syncd
$(SYNCD)_DEPENDS += $(OTN_KVM_LIBSAI_DEB) $(LIBSAIMETADATA_DEV)

# The platform (PMON) HAL driver is implemented natively in the sonic_platform
# python package (sonic-platform-modules-otn-kvm/ols-v/sonic_platform/hal.py),
# so no thrift client/server library is needed anymore.
