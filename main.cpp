#include <Arduino.h>
#include <SoftwareSerial.h> 

const int LIDAR_RX_PIN = 10;
const int LIDAR_TX_PIN = 11;
const long LIDAR_BAUD_RATE = 115200; 
int currentIndex = 0;
int dataArray[360];

SoftwareSerial LidarSerial(LIDAR_RX_PIN, LIDAR_TX_PIN);

typedef struct {
  int distance;
  int strength;
  int temp;
  bool receiveComplete;
} TF;
TF Lidar = {0, 0, 0, false};

// --- Modified data acquisition function ---
void getLidarData(TF* lidar) 
{
  static char i = 0;
  char j = 0;
  int checksum = 0;
  // Change to hold integers for all 9 bytes
  static int rx[9]; 

  // Check the SoftwareSerial port for data
  if (LidarSerial.available()) 
  {
    // Read from the LidarSerial port
    rx[i] = LidarSerial.read();

    if (rx[0] != 0x59) 
    {
      i = 0;
    } 
    else if (i == 1 && rx[1] != 0x59) {
      i = 0;
    } 
    else if (i == 8) 
    {
      for (j = 0; j < 8; j++) 
      {
        checksum += rx[j];
      }
      if (rx[8] == (checksum % 256)) 
      {
          lidar->distance = rx[2] + rx[3] * 256;
          lidar->strength = rx[4] + rx[5] * 256;
          lidar->temp = (rx[6] + rx[7] * 256) / 8 - 256;
          lidar->receiveComplete = true;
      }
      i = 0;
    } 
    else 
    {
      i++;
    }
  }
}

void setup() {
  // Serial for PC Debugging (use 9600 for Serial Monitor)
  Serial.begin(9600);
  // Serial for Lidar Communication (use Lidar's default 115200)
  LidarSerial.begin(LIDAR_BAUD_RATE);
  dataArray[0]=0;


  
  Serial.println("TF-Luna Lidar Test");
}

void printArray(int* array, int size) {
  String dataString = "";
  Serial.println("IMG_START");
  for (int i = 0; i < size; i++) {
    dataString += String(array[i]);
    if (i < size - 1) {
      dataString += ","; 
    }
  }
  Serial.println(dataString);
  Serial.println("IMG_END");
}

void loop() 
{
  getLidarData(&Lidar); 
  if (Lidar.receiveComplete) 
  {

    dataArray[currentIndex] = Lidar.distance;
    Serial.println("Distance at index " + String(currentIndex) + ": " + String(Lidar.distance) + " cm");
    currentIndex = (currentIndex + 1);
    if (currentIndex >= 360) {
      currentIndex = 0;
      printArray(dataArray, 360);
      delay(1000);
      exit(0); 
    }
    Lidar.receiveComplete = false;
    delay(100);
  }
  
}