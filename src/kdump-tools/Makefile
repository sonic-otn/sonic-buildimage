.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

MAIN_TARGET = $(KDUMP_TOOLS)

ifeq ($(CONFIGURED_ARCH),amd64)
TARGET_ARCH=x86_64
else
TARGET_ARCH=$(CONFIGURED_ARCH)
endif
export TARGET_ARCH

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	# Remove any stale files
	#rm -rf ./makedumpfile_$(KDUMP_TOOLS_VERSION_BASE).orig.tar.gz ./makedumpfile_$(KDUMP_TOOLS_VERSION).debian.tar.xz
	rm -rf ./makedumpfile-$(KDUMP_TOOLS_VERSION_BASE)

	# Get makedumpfile release
	#wget http://deb.debian.org/debian/pool/main/m/makedumpfile/makedumpfile_$(KDUMP_TOOLS_VERSION_BASE).orig.tar.gz
	#wget http://deb.debian.org/debian/pool/main/m/makedumpfile/makedumpfile_$(KDUMP_TOOLS_VERSION).debian.tar.xz
	tar -f makedumpfile_$(KDUMP_TOOLS_VERSION_BASE).orig.tar.gz -x
	pushd ./makedumpfile-$(KDUMP_TOOLS_VERSION_BASE)
	tar -f ../makedumpfile_$(KDUMP_TOOLS_VERSION).debian.tar.xz -x

	git init
	git add -f *
	git commit -m "unmodified kdump-tools source"

	# Apply patches
	stg init
	stg import -s ../patch/series

	# Build source and Debian packages
ifeq ($(CROSS_BUILD_ENVIRON), y)
	dpkg-buildpackage -rfakeroot -b -us -uc -a$(CONFIGURED_ARCH) -Pcross,nocheck -j$(SONIC_CONFIG_MAKE_JOBS)  --admindir $(SONIC_DPKG_ADMINDIR)
else
	dpkg-buildpackage -rfakeroot -b -us -uc -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
endif
	popd

	# Move the newly-built .deb packages to the destination directory
	mv $* $(DEST)/
