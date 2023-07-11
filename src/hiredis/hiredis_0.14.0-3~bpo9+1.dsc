-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

Format: 3.0 (quilt)
Source: hiredis
Binary: libhiredis0.14, libhiredis-dev
Architecture: any
Version: 0.14.0-3~bpo9+1
Maintainer: Chris Lamb <lamby@debian.org>
Homepage: https://github.com/redis/hiredis
Standards-Version: 4.2.1
Vcs-Browser: https://salsa.debian.org/lamby/pkg-hiredis
Vcs-Git: https://salsa.debian.org/lamby/pkg-hiredis.git
Testsuite: autopkgtest
Testsuite-Triggers: gcc, libc-dev, pkg-config
Build-Depends: debhelper-compat (= 11), procps <!nocheck>, redis-server (>= 2:2.4.2-2) [linux-any kfreebsd-any] <!nocheck>
Package-List:
 libhiredis-dev deb libdevel optional arch=any
 libhiredis0.14 deb libs optional arch=any
Checksums-Sha1:
 d668b86756d2c68f0527e845dc10ace5a053bbd9 63061 hiredis_0.14.0.orig.tar.gz
 6753e2cad5d3e3d6c0f8553ec8d2738760613227 8464 hiredis_0.14.0-3~bpo9+1.debian.tar.xz
Checksums-Sha256:
 042f965e182b80693015839a9d0278ae73fae5d5d09d8bf6d0e6a39a8c4393bd 63061 hiredis_0.14.0.orig.tar.gz
 f9d400903256b299175e474d8fcd70b295863af3ea248e5f428eb06b0c5213c5 8464 hiredis_0.14.0-3~bpo9+1.debian.tar.xz
Files:
 6d565680a4af0d2e261abbc3e3431b2b 63061 hiredis_0.14.0.orig.tar.gz
 ef340aedc6fd42c549cd503bffb498b2 8464 hiredis_0.14.0-3~bpo9+1.debian.tar.xz

-----BEGIN PGP SIGNATURE-----

iQIzBAEBCAAdFiEEwv5L0nHBObhsUz5GHpU+J9QxHlgFAlvizhsACgkQHpU+J9Qx
HlhA5g//RJKkJYXIXOiAGYMIcMfnbZvMdZ1kJjRSJ7DrXyQ3qimimKII6i6L5eRX
mDFh00cyFNsh8pMUJ2SI0ChOLPYIMUUcGiEF5Ckp0UD3+Dy0aP1Zd6qp38K/kBa1
ERL19iMGMPsLAdEdb/cDKmTO4meUIgoeUrXrOotulndyFYwliGt+9zWtyKg7uuoT
kwPYKrWS8WBnjkIDChrQI4mqQTDPzv+UVfnqZSZFTaSHK4W60hwkg2QqBISJPpdm
tQPV/bVxDHA+QDDqrV+FTJCW9f4iwoXwQbwKt87SLWKJb2emqPMR3QqsAiaBV2Sw
KqOa8ZKrVhm/+1bsrxu/XlV24It4C7E6azw9ySXid7HfcbZVVWYzEWlYi7S2yhAh
Nn7oVNY+EYHcO71CDdBZv8MFZZ+AMV5Uhdftj0bCJ6zzVMw1g7jYMxbOZM+WNHXa
wZU+Bsk+/jySteyjnIsYBgqQRD9CEbo8cfuQ5dFKA/+9YonMXmdsPy/89IzBQWjU
7mEmPz9/OhuQjAby/nvxxvdOWRXctxciqBvX7qCPzDmm9J+kJpNPEYSgPRh7bt/W
Vsq4iYDYR+pVoNjbwtsFLj+64JT7anmjfTF3y61aDAMaBOcOv4AFIoeoYU4kDV2f
buSPFBo30jub/OxyeiUOQ3nC1HUIENp1mih2Rrhyt+QGi+DDzWE=
=3vAR
-----END PGP SIGNATURE-----
