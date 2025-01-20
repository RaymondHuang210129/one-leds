#include <Adafruit_NeoPixel.h>

#include <array>

#include "color.h"
#include "udp_packet_receiver.h"

constexpr int BAUD_RATE = 115200;
constexpr int STACK_SIZE = 8192;

constexpr int PACKET_RECEIVER_PRIORITY = 1;
constexpr int LED_OPERATOR_PRIORITY = 1;

#ifndef LED_STRIP_1_DATA_PIN
#define LED_STRIP_1_DATA_PIN 0
#endif

#ifndef LED_STRIP_1_NUMBER
#define LED_STRIP_1_NUMBER 36
#endif

#ifndef SSID
#define SSID "OpenWrt"
#endif

#ifndef PASSWORD
#define PASSWORD ""
#endif

TaskHandle_t gPacketReceiverTaskHandle;
TaskHandle_t gLedOperatorTaskHandle;

std::array<uint32_t, LED_STRIP_1_NUMBER> gLedsColor;

void setup() {
    Serial.begin(BAUD_RATE);
    Serial.println("Setup");
    xTaskCreatePinnedToCore(packetReceiverTask, "Packet Receiver", STACK_SIZE,
                            NULL, PACKET_RECEIVER_PRIORITY,
                            &gPacketReceiverTaskHandle, 0);

    xTaskCreatePinnedToCore(ledOperatorTask, "LED Operator", STACK_SIZE, NULL,
                            LED_OPERATOR_PRIORITY, &gLedOperatorTaskHandle, 1);
}

void packetReceiverTask(void *pvParameters) {
    Serial.println("Receiver Task");
    UDPPacketReceiver<SSID, PASSWORD, 5005> packetReceiver(
        [&](AsyncUDPPacket packet) {
            auto led_count_in_packet = packet.length() / 3;
            for (size_t led_id = 0;
                 led_id <= led_count_in_packet && led_id < gLedsColor.size();
                 led_id++) {
                gLedsColor.at(led_id) = Adafruit_NeoPixel::Color(
                    packet.data()[led_id * 3], packet.data()[led_id * 3 + 1],
                    packet.data()[led_id * 3 + 2]);
            }
        });
    Serial.println("Packet Receiver Initialized");
    while (true) {
        sleep(10);
    }
}

void ledOperatorTask(void *pvParameters) {
    sleep(5);
    Serial.println("Led Operator Task");
    auto strip =
        Adafruit_NeoPixel(LED_STRIP_1_NUMBER, LED_STRIP_1_DATA_PIN, NEO_GRB);
    strip.begin();
    while (true) {
        usleep(20000);
        for (uint16_t index = 0; index < LED_STRIP_1_NUMBER; index++) {
            strip.setPixelColor(index, gLedsColor.at(index));
        }
        strip.show();
    }
}

void loop() {}
