# OTN libs: fetch .debs from GitHub Releases
# Publish debs at: https://github.com/sonic-otn/sonic-otn-libs/releases
#
# Tag = release/bundle identifier (not package version). Each .deb has its own
# version in the filename (e.g. libsai-otn-1.2.0-amd64.deb).
#   make OTN_LIBS_RELEASE_TAG=latest ...
#   make OTN_LIBS_RELEASE_TAG=release-2024q1 ...
OTN_LIBS_RELEASE_TAG ?=latest
ifeq ($(OTN_LIBS_RELEASE_TAG),latest)
OTN_LIBS_RELEASE_URL = https://github.com/sonic-molex/sonic-otn-libs/releases/latest/download
else
OTN_LIBS_RELEASE_URL = https://github.com/sonic-molex/sonic-otn-libs/releases/download/$(OTN_LIBS_RELEASE_TAG)
endif
