// Design by Nguyen Van Linh
// email: linhnv@kookmin.kr.ac

#include <Adafruit_NeoPixel.h>
#include "DHT.h"//Khai báo thư viện DHT
#include <string.h> 
 
// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN 9
#define DHTPIN 4 //DHT22 pin
#define DHTTYPE DHT22  
DHT dht(DHTPIN, DHTTYPE);
 
// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      64
 
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
//===============
//String fileName;
//int distance = 0;
//int strength = 0;
//boolean receiveComplete = true;
//long data[]={0,0};

void getTFminiData(int* distance, int* strength) {
  static char i = 0;
  char j = 0;
  int checksum = 0; 
  static int rx[9];
  if(Serial.available()) {  
    rx[i] = Serial.read();
    if(rx[0] != 0x59) {
      i = 0;
    } else if(i == 1 && rx[1] != 0x59) {
      i = 0;
    } else if(i == 8) {
      for(j = 0; j < 8; j++) {
        checksum += rx[j];
      }
      if(rx[8] == (checksum % 256)) {
        *distance = rx[2] + rx[3] * 256;
        *strength = rx[4] + rx[5] * 256;
      }
      i = 0;
    } else {
      i++;
    } 
  }  
}
//===================
void setup() 
{
  Serial.begin(115200);
  Serial.println("DHT22 test!");
  dht.begin();
  pixels.begin(); // This initializes the NeoPixel library.
  pixels.show(); 
  pixels.clear();
 
  
}
 
void loop() {
   if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
 
  int distance = 0;
  int strength = 0;

  getTFminiData(&distance, &strength);
  while(!distance) {
    getTFminiData(&distance, &strength);
    if(distance) {
      Serial.print(distance);
      Serial.print("cm\t");
      Serial.print("strength: ");
      Serial.println(strength);
    }
  }
     
 pixels.clear();
 int a[64]= {0,3,4,5,7,56,63,50,51,52,44,42,46,48};
 int h =  ReadH();
 int t = ReadT();
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" *C ");
//Temperature============
      uint8_t bitsCount = sizeof( t ) * 4;
      char str[ bitsCount + 1 ];
      uint8_t i = 0;
      while ( bitsCount-- )
      str[ i++ ] = bitRead( t, bitsCount ) + '0';
      str[ i ] = '\0';
      int arrSize1 = sizeof(str)/sizeof(str[0]);
      int dem=7;
      Serial.println(dem);
      for(int i=0; i<arrSize1 ; i++){
        Serial.println("Temperature: ");
        Serial.println(str);
        if (str[i]=='1')
        {
         // Serial.println(i);
         // a[6]=8;
          a[dem]=i+8;
          //Serial.println(dem);
          dem = dem+1;
        }
        
      }

      //Humidity=============================
      uint8_t bitsCount1 = sizeof( h ) * 4;
      char str1[ bitsCount1 + 1 ];
      uint8_t j = 0;
      while ( bitsCount1-- )
      str1[ j++ ] = bitRead( h, bitsCount1 ) + '0';
      str1[ j ] = '\0';
      char str2[8];
      str2[0]=str1[7]; str2[1]=str1[6]; str2[2]=str1[5]; str2[3]=str1[4]; str2[4]=str1[3]; str2[5]=str1[2]; str2[6]=str1[1]; str2[7]=str1[0]; 
      
    //  Serial.println( str[0] );
    //=======================================
       int arrSize2 = sizeof(str2)/sizeof(str2[0]);
       
       for(int i=0; i<arrSize2 ; i++){
        
        Serial.println("Humidity: ");
        //Serial.println(str1);
        Serial.println(str2);
       // Serial.println(h);
        if (str2[i]=='1')
        {
          //Serial.println(i);
         // a[6]=8;
          a[dem]=i+16;
          dem = dem+1;
        }
        
      }
      ////======================distance
      int d= distance;
      uint8_t bitsCount3 = sizeof( d ) * 4;
      char str3[ bitsCount3 + 1 ];
      uint8_t l = 0;
      while ( bitsCount3-- )
      str3[ l++ ] = bitRead( d, bitsCount3 ) + '0';
      str3[ l ] = '\0';
      int arrSize3 = sizeof(str3)/sizeof(str3[0]);
     // Serial.println(dem);
      for(int i=0; i<arrSize3 ; i++){
        Serial.println("Distance: ");
        Serial.println(str3);
        if (str3[i]=='1')
        {
          Serial.println(i);
         // a[6]=8;
          a[dem]=i+24;
          //Serial.println(dem);
          dem = dem+1;
        }
        
      }

      //================================
    int arrSize = sizeof(a)/sizeof(a[0]);
    for(int i=0; i<arrSize;i++)
    {
      pixels.setPixelColor(a[i], pixels.Color(250,250,250)); // Moderately bright green color
      }
    pixels.show(); // This sends the updated pixel color to the hardware.

 // delay(1000);



}
void DectoBin(int b){
      uint8_t bitsCount = sizeof( b ) * 4;
      char str[ bitsCount + 1 ];
      uint8_t i = 0;
      while ( bitsCount-- )
      str[ i++ ] = bitRead( b, bitsCount ) + '0';
      str[ i ] = '\0';
}
int ReadH(){
   int h = dht.readHumidity();
    return h;
   //delay(1000);
}
int ReadT(){
  int t = dht.readTemperature();
    return t;
      //delay(1000);
   
}
