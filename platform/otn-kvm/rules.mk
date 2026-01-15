include $(PLATFORM_PATH)/hal-server.mk
include $(PLATFORM_PATH)/hal-client.mk
include $(PLATFORM_PATH)/sai.mk
include $(PLATFORM_PATH)/docker-syncd-otn-kvm.mk
include $(PLATFORM_PATH)/platform-modules-otn-kvm.mk
include $(PLATFORM_PATH)/sonic-version.mk
include $(PLATFORM_PATH)/sonic-yanggen.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/onie.mk
include $(PLATFORM_PATH)/kvm-image.mk
include $(PLATFORM_PATH)/raw-image.mk

SONIC_ALL += $(SONIC_ONE_IMAGE) $(SONIC_KVM_IMAGE) $(SONIC_RAW_IMAGE)

# Inject otn-kvm sai into syncd
$(SYNCD)_DEPENDS += $(OTN_KVM_LIBSAI_DEB) $(LIBSAIMETADATA_DEV)

# Inject otn-kvm hal dependency library into pmon
$(DOCKER_PLATFORM_MONITOR)_DEPENDS += $(OTN_KVM_HALCLIENT_DEB)
