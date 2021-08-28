// A basic everyday NeoPixel strip test program.

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1:
#define LED_PIN    6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 300

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


// setup() function -- runs once at startup --------------------------------

void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(255); // Set BRIGHTNESS (max = 255)
  Serial.begin(9600);
  Serial.setTimeout(100);
}

void loop() {
  char function = Serial.read();
  if(function == 'd') serialDraw();
  if(function == 'f') serialFill();
  if(function == 'c') serialSetColor();
  if(function == 's') strip.show();
}

int color = strip.Color(0, 0, 0);
void serialSetColor() {
  int r = Serial.parseInt();
  int g = Serial.parseInt();
  int b = Serial.parseInt();
  color =  strip.Color(r, g, b);
}

void serialDraw() {
  int i = Serial.parseInt();
  int r = Serial.parseInt();
  int g = Serial.parseInt();
  int b = Serial.parseInt();
  strip.setPixelColor(i, strip.Color(r, g, b));
}

void serialFill() {
  int i = Serial.parseInt();
  int n = Serial.parseInt();
  int r = Serial.parseInt();
  int g = Serial.parseInt();
  int b = Serial.parseInt();
  strip.fill(strip.Color(r, g, b), i, n);
}
