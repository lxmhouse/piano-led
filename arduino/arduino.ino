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
  Serial.setTimeout(10);
  // colorWipe(strip.Color(255, 0, 0), 1); // Red
  // black();
  // white();
}

void loop()
{
  // Check if data is available to read.
  if (Serial.available() > 0)
  {
    // Read the data in and convert it to an integer.
    String notes = Serial.readStringUntil('\n');

    // int note = Serial.readString().toInt();
    // black();

    int noteVec[50]; // Manually managed array. You might need to adjust the size.
    int size = parseData(notes, noteVec);
    struct Color
    {
      String name;
      uint32_t value;
    };
    const Color colorMap[] = {{"red", 0x58},
                              {"orange", 0x1C},
                              {"yellow", 0x18},
                              {"green", 0x59},
                              {"lightgreen", 0x55},
                              {"darkblue", 0x45},
                              {"blue", 0x49},
                              {"turquoise", 0x19},
                              {"clearblue", 0x51},
                              {"darkpurple", 0x4D},
                              {"purple", 0x1E},
                              {"magenta", 0x1A},
                              {"pink", 0x4C},
                              {"seablue", 0x1D},
                              {"lightblue", 0x1B},
                              {"verylightblue", 0x1F}};

    // CLOUD
    for (int i = 0; i < size; i++)
    {
      int idx = noteVec[i] % NUM_PIXELS;
      strip.setPixelColor(idx, random(0, 255), random(0, 255), random(0, 255), 0);
    }
  }
}