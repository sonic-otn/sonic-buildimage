CC=gcc
CFLAGS += -std=gnu99 -D_GNU_SOURCE

CXX=g++
CXXFLAGS += -std=c++11 -D_GNU_SOURCE
LDFLAGS += -lpthread -lboost_filesystem -lboost_system -lgtest

BINARY = systemd-sonic-generator

$(BINARY): systemd-sonic-generator.c
	rm -f ./systemd-sonic-generator

	$(CC) $(CFLAGS) -o $@ $^

install: $(BINARY)
	mkdir -p $(DESTDIR)
	mkdir -p $(DESTDIR)/lib
	mkdir -p $(DESTDIR)/lib/systemd
	mkdir -p $(DESTDIR)/lib/systemd/system-generators
	cp ./systemd-sonic-generator $(DESTDIR)/lib/systemd/system-generators
