HALCLIENT_VERSION = 1.0.0
OTN_KVM_HALCLIENT_DEB = libhalplatformclient-otn-$(HALCLIENT_VERSION)-amd64.deb
$(OTN_KVM_HALCLIENT_DEB)_URL = "https://raw.githubusercontent.com/sonic-otn/sonic-otn-libs/refs/heads/main/debs/$(OTN_KVM_HALCLIENT_DEB)"

SONIC_ONLINE_DEBS += $(OTN_KVM_HALCLIENT_DEB)
