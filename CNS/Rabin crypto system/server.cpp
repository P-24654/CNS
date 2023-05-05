#include <arpa/inet.h>
#include <cstring>
#include <iostream>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

// Include Rabin Cryptosystem library
// Replace this with the actual Rabin Cryptosystem library
#include "rabin_system.h"

#define PORT 8080

int main() {
    int sockfd, newsockfd;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t clilen;
    char buffer[1024] = {0};

    // Create socket
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        return 1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(PORT);

    // Bind the socket to a specific address and port
    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("bind failed");
        return 1;
    }

    // Listen for incoming connections
    if (listen(sockfd, 5) < 0) {
        perror("listen failed");
        return 1;
    }

    std::cout << "Server listening on port " << PORT << "..." << std::endl;

    clilen = sizeof(cli_addr);

    // Accept incoming connections
    if ((newsockfd = accept(sockfd, (struct sockaddr *)&cli_addr, &clilen)) < 0) {
        perror("accept failed");
        return 1;
    }

    std::cout << "Connection established with client " << inet_ntoa(cli_addr.sin_addr) << std::endl;

    while (true) {
        // Receive data from client
        int bytes_read = read(newsockfd, buffer, sizeof(buffer));
        if (bytes_read < 0) {
            perror("read failed");
            return 1;
        } else if (bytes_read == 0) {
            std::cout << "Client disconnected" << std::endl;
            break;
        }

        string rec_data = lab_6_rabin_system::decrypt(buffer);

        std::cout << "Received: " << rec_data << std::endl;

        // Perform Rabin Cryptosystem encryption
        // Replace this with the actual Rabin Cryptosystem implementation
        std::string encrypted_data = lab_6_rabin_system::encrypt(std::string(buffer));

        // Send encrypted data to client
        int bytes_sent = send(newsockfd, encrypted_data.c_str(), encrypted_data.length(), 0);
        if (bytes_sent < 0) {
            perror("send failed");
            return 1;
        }
    }

    close(newsockfd);
    close(sockfd);

    return 0;
}
