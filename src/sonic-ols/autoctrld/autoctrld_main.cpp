#include <iostream>
#include <signal.h>
#include <unistd.h>

bool running = true;

void signalHandler(int signum) {
    std::cout << "Interrupt signal (" << signum << ") received." << std::endl;
    running = false;
}

int main(int argc, char* argv[]) {
    std::cout << "autoctrld starting..." << std::endl;
    
    // Register signal handler
    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);
    
    // Main loop
    while (running) {
        sleep(1);
    }
    
    std::cout << "autoctrld stopped." << std::endl;
    return 0;
}
