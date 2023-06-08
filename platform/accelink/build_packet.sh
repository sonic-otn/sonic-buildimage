#!/bin/bash

export IMAGE_VERSION="${SONIC_IMAGE_VERSION}"

export B_NUMBER=`printf "%03d" ${BUILD_NUMBER}`

########### recognize p230c latest bin  ##############
p230c_binaries=(`ls binaries/P230C/latest`)
export p230c_latest_bin=${p230c_binaries[0]}

########### recognize e110c latest bin  ##############
e110c_binaries=(`ls binaries/E110C/latest`)
export e110c_latest_bin=${e110c_binaries[0]}

########### recognize fpga-up latest bin  ##############
fpga_up_binaries=(`ls binaries/FPGA_UP/latest`)
export fpga_up_latest_bin=${fpga_up_binaries[0]}

########### recognize fpga-up-x86 latest bin  ##############
fpga_up_x86_binaries=(`ls binaries/FPGA_UP_X86/latest`)
export fpga_up_x86_latest_bin=${fpga_up_x86_binaries[0]}

########### recognize fpga-down latest bin  ##############
fpga_down_binaries=(`ls binaries/FPGA_DOWN/latest`)
export fpga_down_latest_bin=${fpga_down_binaries[0]}

export sonicfile=OBX1100E-V100R001C000B${B_NUMBER}
mkdir -p /tmp/${sonicfile}/

pushd /tmp

cp /sonic/target/sonic-accelink.bin ${sonicfile}
export SONIC_BIN_MD5=`md5sum /tmp/${sonicfile}/sonic-accelink.bin | awk -F ' ' '{print $1}'`

cp /sonic/binaries/P230C/latest/${p230c_latest_bin}/DCI_OBX1100_P230.bin ${sonicfile}
export P230C_BIN_MD5=`md5sum /tmp/${sonicfile}/DCI_OBX1100_P230.bin | awk -F ' ' '{print $1}'`

cp /sonic/binaries/E110C/latest/${e110c_latest_bin}/DCI_OEX1000_E110.bin ${sonicfile}
export E110C_BIN_MD5=`md5sum /tmp/${sonicfile}/DCI_OEX1000_E110.bin | awk -F ' ' '{print $1}'`

cp /sonic/binaries/FPGA_UP/latest/${fpga_up_latest_bin}/output_file_auto.rpd ${sonicfile}
export FPGA_UP_BIN_MD5=`md5sum /tmp/${sonicfile}/output_file_auto.rpd | awk -F ' ' '{print $1}'`

cp /sonic/binaries/FPGA_UP_X86/latest/${fpga_up_x86_latest_bin}/output_file_cfm1_auto.rpd ${sonicfile}
export FPGA_UP_X86_BIN_MD5=`md5sum /tmp/${sonicfile}/output_file_cfm1_auto.rpd | awk -F ' ' '{print $1}'`

cp /sonic/binaries/FPGA_DOWN/latest/${fpga_down_latest_bin}/fpga_burn.bin ${sonicfile}
export FPGA_DOWN_BIN_MD5=`md5sum /tmp/${sonicfile}/fpga_burn.bin | awk -F ' ' '{print $1}'`

j2 /sonic/files/build_templates/upgradecfg.j2 > ${sonicfile}/upgradecfg

tar -cvzf ${sonicfile}.tar.gz ${sonicfile}
mv ${sonicfile}.tar.gz /sonic/target/
rm -rf ${sonicfile}
popd


