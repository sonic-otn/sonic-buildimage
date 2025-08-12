ONIE_RECOVERY_IMAGE = onie-recovery-x86_64-otn-kvm_x86_64-r0.iso
$(ONIE_RECOVERY_IMAGE)_URL = "https://raw.githubusercontent.com/sonic-molex/ot_kvm_onie/refs/heads/otn/$(ONIE_RECOVERY_IMAGE)"

SONIC_ONLINE_FILES += $(ONIE_RECOVERY_IMAGE)
