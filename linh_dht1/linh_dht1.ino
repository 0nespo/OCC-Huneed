#include <Adafruit_NeoPixel.h>
#include "DHT.h"//DHT
#include <string.h> 
 
// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN 9
#define DHTPIN 4 //DHT22 pin
#define DHTTYPE DHT22  
#define Dig_pin 6;
int Dig_out = LOW;
int v = 0;
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
     
 pixels.clear();
 int a[64]= {0,3,4,5,7,56,63,50,51,52,44,42,46,48};
 int h =  ReadH();
 int t = ReadT();
 int v = ReadV();
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print("Vibration: ");
  Serial.print(v);
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
      
      ///Vibration=====================
      //int v = Ana_out;
      uint8_t bitsCount4 = sizeof( v ) * 4;
      char str3[ bitsCount4 + 1 ];
      uint8_t m = 0;
      while ( bitsCount4-- )
      str3[ m++ ] = bitRead( v, bitsCount4 ) + '0';
      str3[ m ] = '\0';
      char str4[8];
      str4[0]=str3[7]; str4[1]=str3[6]; str4[2]=str3[5]; str4[3]=str3[4]; str4[4]=str3[3]; str4[5]=str3[2]; str4[6]=str3[1]; str4[7]=str3[0]; 
       
      int arrSize4 = sizeof(str4)/sizeof(str4[0]);
     // Serial.println(dem);
      for(int i=0; i<arrSize4 ; i++){
        Serial.println("Vibration: ");
        //Serial.println(str3);

        Serial.println(str4);
        Serial.println(v); // (v-100)

        if (str4[i]=='1')
        {
          Serial.println(i);
         // a[6]=8;
          a[dem]=i+32;
          //Serial.println(dem);
          dem = dem+3;
        }

      //================================
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
int ReadV(){
   v = analogRead(A1);
   return v;
   //delay(1000);
}
