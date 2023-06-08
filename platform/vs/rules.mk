include $(PLATFORM_PATH)/syncd-vs.mk
include $(PLATFORM_PATH)/sonic-version.mk
include $(PLATFORM_PATH)/docker-sonic-vs.mk
include $(PLATFORM_PATH)/docker-syncd-vs.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/onie.mk
include $(PLATFORM_PATH)/kvm-4-slot-factory-config.mk
include $(PLATFORM_PATH)/kvm-image.mk

VSCMD = vscmd
$(VSCMD)_PATH = /sonic/platform/vs/docker-sonic-vs

DSSERVE = dsserve
$(DSSERVE)_URL = "https://sonicstorage.blob.core.windows.net/packages/20190307/dsserve?sv=2015-04-05&sr=b&sig=lk7BH3DtW%2F5ehc0Rkqfga%2BUCABI0UzQmDamBsZH9K6w%3D&se=2038-05-06T22%3A34%3A45Z&sp=r"

SONIC_COPY_FILES += $(VSCMD)
SONIC_ONLINE_FILES += $(DSSERVE)

SONIC_ALL += $(SONIC_ONE_IMAGE) $(SONIC_KVM_IMAGE) $(DOCKER_SONIC_VS)
