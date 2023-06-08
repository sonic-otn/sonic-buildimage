.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

include asic.conf
export NUM_ASIC

subdirs := e100c e110c e120c p230c
include Make.subdirs

MAIN_TARGET = obx1100-factory-config_1.0.0_all.deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% : ${subdirs}
	dpkg-buildpackage -rfakeroot -b -us -uc -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	mv ../$* $(DEST)/




