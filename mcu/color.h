#include <Adafruit_NeoPixel.h>

class Color {
   public:
    Color(uint8_t red, uint8_t green, uint8_t blue)
        : m_red(red), m_green(green), m_blue(blue) {}
    Color() : m_red(0), m_green(0), m_blue(0) {}

    uint32_t pack() { return Adafruit_NeoPixel::Color(m_red, m_green, m_blue); }

   private:
    uint8_t m_red;
    uint8_t m_green;
    uint8_t m_blue;
};
