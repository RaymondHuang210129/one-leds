#include <AsyncUDP.h>
#include <WiFi.h>

#include <array>
#include <functional>

template <const char* SSID, const char* Password, unsigned short Port>
class UDPPacketReceiver {
   public:
    UDPPacketReceiver(const AuPacketHandlerFunction& callback) {
        WiFi.disconnect();

        WiFi.begin(SSID, Password);
        while (WiFi.waitForConnectResult() != WL_CONNECTED) {
            Serial.println("Connecting");
            sleep(1);
        }
        Serial.println("Connected");

        if (!mUdp.listen(Port)) {
            Serial.print("Failed to listen to port");
            Serial.print(Port);
        }
        Serial.println("Waiting for UDP packet");
        mUdp.onPacket(callback);
    }

   private:
    AsyncUDP mUdp;
};
