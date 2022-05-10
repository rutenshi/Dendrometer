/*
  Send data got from sensor to TTN
*/
#include "LoRaWan_APP.h"
#include "Arduino.h"
#include <stdlib.h>

// LORAWAN_NETMODE
// OTAA
// get values from application
uint8_t devEui[] = { 0x22, 0x32, 0x33, 0x00, 0x00, 0x88, 0x88, 0x02 };
uint8_t appEui[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05 };
uint8_t appKey[] = { 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x66, 0x01 };
// ABP
uint8_t nwkSKey[] = { 0x9b, 0xee, 0x6e, 0xc4, 0x43, 0xda, 0xd4, 0x4a, 0x13, 0x45, 0x6a, 0xf6, 0x6e, 0xf1, 0x5c,0x36 };
uint8_t appSKey[] = { 0x30, 0x19, 0xfa, 0x19, 0xfa, 0x50, 0x65, 0x36, 0xe6, 0xde, 0x0a, 0x47, 0x47, 0xd8, 0xf2,0x3d };
uint32_t devAddr =  ( uint32_t )0x260bf90b;

// LoraWan channelsmask, default channels 0-7
uint16_t userChannelsMask[6] = { 0x00FF,0x0000,0x0000,0x0000,0x0000,0x0000 };

// LoraWan region, select in arduino IDE tools
LoRaMacRegion_t loraWanRegion = ACTIVE_REGION; //EU_868

// LoraWan Class, Class A and Class C are supported
DeviceClass_t  loraWanClass = LORAWAN_CLASS; //CLASS_A

// the application data transmission duty cycle.  value in [ms].
uint32_t appTxDutyCycle = 1*60*1000; //1 minute

// OTAA or ABP
bool overTheAirActivation = LORAWAN_NETMODE; //OTAA

// ADR enable
bool loraWanAdr = LORAWAN_ADR;

// set LORAWAN_Net_Reserve ON, the node could save the network info to flash, when node reset not need to join again
bool keepNet = LORAWAN_NET_RESERVE;

// Indicates if the node is sending confirmed or unconfirmed messages
bool isTxConfirmed = LORAWAN_UPLINKMODE; //unconfirmed messages

// Application port
uint8_t appPort = 2;

/*
Number of trials to transmit the frame, if the LoRaMAC layer did not
receive an acknowledgment. The MAC performs a datarate adaptation,
according to the LoRaWAN Specification V1.0.2, chapter 18.4, according
to the following table:

Transmission nb | Data Rate
----------------|-----------
1 (first)       | DR
2               | DR
3               | max(DR-1,0)
4               | max(DR-1,0)
5               | max(DR-2,0)
6               | max(DR-2,0)
7               | max(DR-3,0)
8               | max(DR-3,0)

Note, that if NbTrials is set to 1 or 2, the MAC will not decrease
the datarate, in case the LoRaMAC layer did not receive an acknowledgment
*/

//unsigned integer of length 8 bits (1 byte), it's a byte with 8 bits no matter which platform the program runs on
uint8_t confirmedNbTrials = 4; 

// Prepares the payload of the frame
static void prepareTxFrame( uint8_t port ){
  // define variable to get micrometer value
  float d_um = 0;

  //------ insert code here to obtain micrometer from sensor -------

  
  //-----------------------------------------------------------------
  //convert variable d_um from float to char type
  //5 means the total of digits and 2 the amount of decimal numbers-->0000.00
  // check the size of tempstring due to maximum payload size depending on the spreding factor
  char tempstring[20]; //temporal variable to store the whole number as string
  dtostrf(d_um, 5, 2, tempstring); // turn float into char, save it to tempstring
  //Create object "micrometer" as String and introduce tempstring array
  String micrometer(tempstring);
  
  Serial.println();
  // Show on Serial Monitor the bytes in hexadecimal format to be sent
  Serial.print("Sending um: " + micrometer + " --> ");
  for (unsigned int j = 0; j < micrometer.length(); j++) {
    // move bites to the right and just keep the unit number, (check ascii hex from 30 = 0 to 39 = 9)
    Serial.print(micrometer[j] >> 4, HEX); 
    Serial.print(micrometer[j] & 0xF, HEX);
    Serial.print(" ");
  }
  Serial.println();
  
}



void setup() {
 
  // Initialize serial port communication
  Serial.begin(115200);
 
  #if(AT_SUPPORT)
  enableAt(); // if LORAWAN_AT_SUPPORT: "ON" enables AT COMMANDS
  #endif
  deviceState = DEVICE_STATE_INIT; // Initialize device
  LoRaWAN.ifskipjoin(); // if saved net info is OK in lorawan mode, skip join.
 
}

void loop() {

    switch( deviceState ) {
    //DEVICE_STATE_INIT
    case DEVICE_STATE_INIT: {
#if(LORAWAN_DEVEUI_AUTO)
      LoRaWAN.generateDeveuiByChipID(); // if we don't select LORAWAN_DEVEUI: "CUSTOM", default is "GenerateByChipID"
#endif

#if(AT_SUPPORT)
      getDevParam();
#endif
      printDevParam();
      LoRaWAN.init(loraWanClass, loraWanRegion); //CLASS_A, REGION_EU868
      deviceState = DEVICE_STATE_JOIN;
      break;
    }
    //DEVICE_STATE_JOIN
    case DEVICE_STATE_JOIN: { //
      LoRaWAN.join(); // depends on the activation method LORAWAN_NETMODE: *OTAA (Over The Air Activation), *ABP
      break;
    }
    //
    case DEVICE_STATE_SEND: {
      prepareTxFrame( appPort );
      LoRaWAN.send();
      deviceState = DEVICE_STATE_CYCLE;
      break;
    }
    //DEVICE_STATE_CYCLE
    case DEVICE_STATE_CYCLE: {
      // Schedule next packet transmission
      txDutyCycleTime = appTxDutyCycle + randr( 0, APP_TX_DUTYCYCLE_RND );
      LoRaWAN.cycle(txDutyCycleTime);
      deviceState = DEVICE_STATE_SLEEP;
      break;
    }
    //DEVICE_STATE_SLEEP
    case DEVICE_STATE_SLEEP: {
      LoRaWAN.sleep();
      break;
    }
    //DEVICE_STATE_INIT
    default: {
      deviceState = DEVICE_STATE_INIT;
      break;
    }
   
  }
    
}
