#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_PIXELS 24

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRBW + NEO_KHZ800);

int parseData(String data, int *intList)
{
  char *chrArray = strdup(data.c_str());
  int i = 0;

  char *token = strtok(chrArray, ",");
  while (token != NULL)
  {
    intList[i] = atoi(token);
    i++;
    token = strtok(NULL, ",");
  }

  free(chrArray);
  return i; // Return size of filled data in intList
}

void setup()
{

  strip.begin();
  strip.setBrightness(20);
  strip.show();

  // Begin serial communication.
  Serial.begin(9600);
  Serial.setTimeout(10); // reduce the latency of the serial communication to 10 ms (default is 1 second)
  white();
}

void loop()
{
  // Check if data is available to read.
  if (Serial.available() > 0)
  {
    // Read the data in and convert it to an integer.
    String notes = Serial.readStringUntil('\n');

    // int note = Serial.readString().toInt();
    black();

    int noteVec[50]; // Manually managed array. You might need to adjust the size.
    int size = parseData(notes, noteVec);
    for (int i = 0; i < size; i++)
    {
      int idx = noteVec[i] % NUM_PIXELS;
      strip.setPixelColor(idx, random(0, 255), random(0, 255), random(0, 255), 0);
    }

    // Show the changes on the strip.
    strip.show();
  }
}

void white()
{
  for (uint16_t i = 0; i < strip.numPixels(); i++)
  {
    strip.setPixelColor(i, 0, 0, 0, 255);
  }
  strip.show();
}

void black()
{
  for (uint16_t i = 0; i < strip.numPixels(); i++)
  {
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait)
{
  for (uint16_t i = 0; i < strip.numPixels(); i++)
  {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }

  strip.show();
}

void theaterChase(uint32_t c, uint8_t wait)
{
  for (int j = 0; j < 10; j++)
  {
    for (int q = 0; q < 3; q++)
    {
      for (uint16_t i = 0; i < strip.numPixels(); i = i + 3)
      {
        strip.setPixelColor(i + q, c);
      }
      strip.show();

      delay(wait);

      for (uint16_t i = 0; i < strip.numPixels(); i = i + 3)
      {
        strip.setPixelColor(i + q, 0);
      }
    }
  }
}
