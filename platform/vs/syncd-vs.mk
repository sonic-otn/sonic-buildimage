$(LIBLAIREDIS)_DPKG_TARGET = binary-syncd-vs

SYNCD_VS = syncd-vs_1.0.0_$(CONFIGURED_ARCH).deb
$(SYNCD_VS)_RDEPENDS += $(LIBLAIREDIS) $(LIBLAIMETADATA) $(LIBLAIVS)
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(SYNCD_VS)))

SYNCD_VS_DBG = syncd-vs-dbg_1.0.0_$(CONFIGURED_ARCH).deb
$(SYNCD_VS_DBG)_DEPENDS += $(SYNCD_VS)
$(SYNCD_VS_DBG)_RDEPENDS += $(SYNCD_VS)
$(eval $(call add_derived_package,$(LIBLAIREDIS),$(SYNCD_VS_DBG)))
