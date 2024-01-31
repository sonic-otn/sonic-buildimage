ONIE_RECOVERY_IMAGE = onie-recovery-x86_64-ot_kvm_x86_64-r0.iso
$(ONIE_RECOVERY_IMAGE)_URL = "https://github.com/sonic-otn/ot_kvm_onie/releases/download/v1.0/onie-recovery-x86_64-ot_kvm_x86_64-r0.iso"

ONIE_RECOVERY_KVM_4ASIC_IMAGE = onie-recovery-x86_64-ot_kvm_x86_64_4_asic-r0.iso
$(ONIE_RECOVERY_KVM_4ASIC_IMAGE)_URL = "https://github.com/sonic-otn/ot_kvm_onie/releases/download/v1.0/onie-recovery-x86_64-ot_kvm_x86_64_4_asic-r0.iso"

ONIE_RECOVERY_KVM_6ASIC_IMAGE = onie-recovery-x86_64-ot_kvm_x86_64_6_asic-r0.iso
$(ONIE_RECOVERY_KVM_6ASIC_IMAGE)_URL = "https://github.com/sonic-otn/ot_kvm_onie/releases/download/v1.0/onie-recovery-x86_64-ot_kvm_x86_64_6_asic-r0.iso"

SONIC_ONLINE_FILES += $(ONIE_RECOVERY_IMAGE) $(ONIE_RECOVERY_KVM_4ASIC_IMAGE) $(ONIE_RECOVERY_KVM_6ASIC_IMAGE)
