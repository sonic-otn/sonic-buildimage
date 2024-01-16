$(LIBOTAIREDIS)_DPKG_TARGET = binary-syncd-ot-vs

SYNCD_OT_VS = syncd-ot-vs_1.0.0_$(CONFIGURED_ARCH).deb
$(SYNCD_OT_VS)_RDEPENDS += $(LIBOTAIREDIS) $(LIBOTAIMETADATA) $(LIBOTAIVS)
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(SYNCD_OT_VS)))

SYNCD_OT_VS_DBG = syncd-ot-vs-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(SYNCD_OT_VS_DBG)_DEPENDS += $(SYNCD_OT_VS)
$(SYNCD_OT_VS_DBG)_RDEPENDS += $(SYNCD_OT_VS)
$(eval $(call add_derived_package,$(LIBOTAIREDIS),$(SYNCD_OT_VS_DBG)))
