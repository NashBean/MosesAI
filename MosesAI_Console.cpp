#include <iostream>
#include <string>
#include <curl/curl.h>
#include <jsoncpp/json/json.h>  // For JSON parsing (install libjsoncpp-dev)

// Version
int MAJOR_VERSIOM = 0;
int MINOR_VERSION = 3;
int FIX_VERSION = 0;
//VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

std::string AI_NAME = "MosesAI";

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

int main() {
    std::cout << AI_NAME << " Console v'<<MAJOR_VERSIOM<<'.'<<MINOR_VERSION<<'.'<<FIX_VERSION<<' - Type 'exit' to quit or 'learn [topic]' for self-research" << std::endl;
    CURL *curl = curl_easy_init();
    if (!curl) {
        std::cerr << "CURL init failed" << std::endl;
        return 1;
    }

    std::string response;
    while (true) {
        std::string query;
        std::cout << "You: ";
        std::getline(std::cin, query);
        if (query == "exit") break;

        // Handle "learn [topic]" command
        std::string post_data;
        if (query.substr(0, 6) == "learn ") {
            std::string topic = query.substr(6);
            post_data = "{\"query\": \"learn " + topic + "\"}";
        } else {
            post_data = "{\"query\": \"" + query + "\"}";
        }

        response.clear();
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5001/ask");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        CURLcode res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "Request failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            Json::Value json_response;
            Json::Reader reader;
            reader.parse(response, json_response);
            std::string ai_response = json_response.get("response", "No response").asString();
            std::cout << AI_NAME << ": " << ai_response << std::endl;
            // Speak (espeak -v mb-us1)
            system(("espeak -v mb-us1 \"" + ai_response + "\"").c_str());
        }
    }

    curl_easy_cleanup(curl);
    return 0;
}