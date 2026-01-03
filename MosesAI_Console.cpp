#include <iostream>
#include <string>
#include <curl/curl.h>

// Version
int MAJOR_VERSIOM = 0;
int MINOR_VERSION = 1;
int FIX_VERSION = 0;
//VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

int main() {
    std::cout << "MosesAI Console - Type 'exit' to quit" << std::endl;
    CURL *curl = curl_easy_init();
    if (!curl) {
        std::cerr << "CURL init failed" << std::endl;
        return 1;
    }

    while (true) {
        std::string query;
        std::cout << "You: ";
        std::getline(std::cin, query);
        if (query == "exit") break;

        std::string post_data = "{\"query\": \"" + query + "\"}";
        std::string response;
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5002/ask");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        CURLcode res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "Request failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "MosesAI: " << response << std::endl;
            // Speak (espeak -v mb-us1)
            system(("espeak -v mb-us1 \"" + response + "\"").c_str());
        }
    }

    curl_easy_cleanup(curl);
    return 0;
}