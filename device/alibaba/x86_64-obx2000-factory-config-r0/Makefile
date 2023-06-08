.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

include asic.conf
export NUM_ASIC

subdirs := oa2325 oa2335 ocm8 otdr8
include Make.subdirs

MAIN_TARGET = obx2000-factory-config_1.0.0_all.deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% : ${subdirs}
	dpkg-buildpackage -rfakeroot -b -us -uc -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	mv ../$* $(DEST)/

