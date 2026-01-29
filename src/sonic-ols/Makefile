RM := rm -f
AUTOCTRLD_TARGET := autoctrld/autoctrld
WLD_TARGET := wld/wld

CP := cp
MKDIR := mkdir
CC := g++
LIBS := -levent -lhiredis -lswsscommon -lpthread -lboost_thread -lboost_system -lzmq -lboost_serialization

CFLAGS += -Wall -std=c++17 -fPIE -I$(PWD)/../sonic-swss-common/common
LDFLAGS += -pie

PWD := $(shell pwd)

# Source files
AUTOCTRLD_SRCS := autoctrld/autoctrld_main.cpp
AUTOCTRLD_OBJS := $(AUTOCTRLD_SRCS:.cpp=.o)

WLD_SRCS := wld/wld_main.cpp
WLD_OBJS := $(WLD_SRCS:.cpp=.o)

all: sonic-autoctrld sonic-wld

sonic-autoctrld: $(AUTOCTRLD_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: G++ Linker'
	$(CC) $(LDFLAGS) -o $(AUTOCTRLD_TARGET) $(AUTOCTRLD_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '

sonic-wld: $(WLD_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: G++ Linker'
	$(CC) $(LDFLAGS) -o $(WLD_TARGET) $(WLD_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '

%.o: %.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: G++ Compiler'
	$(CC) $(CFLAGS) -c -o $@ $<
	@echo 'Finished building: $<'
	@echo ' '

install:
	$(MKDIR) -p $(DESTDIR)/usr/bin
	$(CP) $(AUTOCTRLD_TARGET) $(DESTDIR)/usr/bin/autoctrld
	$(CP) $(WLD_TARGET) $(DESTDIR)/usr/bin/wld

deinstall:
	$(RM) $(DESTDIR)/usr/bin/autoctrld
	$(RM) $(DESTDIR)/usr/bin/wld

clean:
	-$(RM) $(AUTOCTRLD_TARGET) $(AUTOCTRLD_OBJS) $(WLD_TARGET) $(WLD_OBJS)
	-@echo ' '

.PHONY: all clean install deinstall
