#include <IRremote.h>
#define IR_SEND_PIN 3

IRsend irsend(IR_SEND_PIN);

struct Color
{
  String name;
  uint8_t value;
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
  // Begin serial communication.
  Serial.begin(9600);
  Serial.setTimeout(10);

  irsend.begin(IR_SEND_PIN); // Send a 500us IR pulse
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

    // CLOUD
    // for (int i = 0; i < size; i++)
    // {
    // int idx = noteVec[-1] % NUM_PIXELS;
    int colorIdx = noteVec[size - 1] % 12;    // Get the second to last value in noteVec modulo 12
    uint8_t color = colorMap[colorIdx].value; // Get the corresponding hex value from colorMap
    uint8_t address = 0x00;                   // Most significant 8 bits of address; 0x00 for single address
    irsend.sendNEC(address, color, 1);        // 0 indicates no repeat
                                              // delay(2);
    // }
  }
}