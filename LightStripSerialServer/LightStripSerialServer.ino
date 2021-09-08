// A basic everyday NeoPixel strip test program.

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1:
#define LED_PIN    6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 263

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)


char serialReadWait(){
  while (true) {
    if(Serial.available() > 0) return Serial.read();
    delay(0.001);
  }
}

bool invertedIndexing = true;
void flipIndexingMode() {
  invertedIndexing = !invertedIndexing;
}
int toIndex(int parsedInt) {
  int maxIndex = LED_COUNT - 1;
  return invertedIndexing ?
    maxIndex - (parsedInt % LED_COUNT) :
    parsedInt % LED_COUNT;
}

void setup() {
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(255); // Set BRIGHTNESS (max = 255)
  Serial.begin(230400);
  Serial.setTimeout(100);
}

void loop() {
  char function = Serial.read();
  if(function == 'b') serialSetBackground();
  if(function == 'd') serialDraw();
  if(function == 'f') serialFill();
  if(function == 'c') serialSetColor();
  if(function == 's') strip.show();
  if(function == 'i') flipIndexingMode();
}

uint32_t color = strip.Color(0, 0, 0);
void serialSetColor() {
  color = serialParseColor();
}

void serialSetBackground() {
  strip.fill(serialParseColor(), 0, 300);
}

uint32_t serialParseColor() {
  String r, g, b;
  r = g = b = "";
  r.concat(serialReadWait());
  r.concat(serialReadWait());
  g.concat(serialReadWait());
  g.concat(serialReadWait());
  b.concat(serialReadWait());
  b.concat(serialReadWait());
  int rint = strtol(r.c_str(), NULL, 16);
  int gint = strtol(g.c_str(), NULL, 16);
  int bint = strtol(b.c_str(), NULL, 16);
  return strip.Color(
    rint,
    gint,
    bint);
}

void serialDraw() {
  int i = toIndex(Serial.parseInt());
  strip.setPixelColor(i, color);
}

// This function is a little busted. Some off by 1 errors
void serialFill() {
  int i = toIndex(Serial.parseInt());
  int n = Serial.parseInt();
  if (invertedIndexing) {
    strip.fill(color, i - n+1, n);
  }
  else {
    strip.fill(color, i, n);
  }
}
