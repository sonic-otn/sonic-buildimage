P230C_HOME=$(CURDIR)
export P230C_HOME

TEMPLATE_FILE=${P230C_HOME}/laiobject.json.j2
export TEMPLATE_FILE

TEMPLATE_DIR=${P230C_HOME}
export TEMPLATE_DIR

subdirs := L1_400G_CA_100GE LA_200G_CA_100GE_QPSK
include Make.subdirs 

all::
	@(j2 flexcounter.json.j2 > flexcounter.json;)
