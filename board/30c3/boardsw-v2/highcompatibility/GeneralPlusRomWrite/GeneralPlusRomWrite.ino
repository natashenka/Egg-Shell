#include <SPI.h>

#define SLAVESELECT 17//ss

//opcodes
#define WREN  6
#define WRDI  4
#define RDSR  5
#define WRSR  1
#define READ  3
#define WRITE 2
#define SECTOR_ERASE 0xd8

long int once = 0;

void setup()
{
  Serial.begin(115200);

  SPI.begin();
  digitalWrite(SLAVESELECT, HIGH); //disable device
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));

  while (!Serial) {}
  Serial.print("serial test \r\n");
}

void loop()
{
  long int i;
  byte b[256];
  byte status_reg = 0;

  for (i = 0; i < 256; ) {
    i += Serial.readBytes((char*)b+i, 16);
    Serial.println(".");
  }

  if ((once % 256) == 0) {
    // eeprom_output_data = read_eeprom(address);
    Serial.print("Sector erase: ");
    Serial.println(once / 256);
    digitalWrite(SLAVESELECT, LOW);
    SPI.transfer(WREN);  // Write enable
    digitalWrite(SLAVESELECT, HIGH);

    digitalWrite(SLAVESELECT, LOW);
    SPI.transfer(RDSR);
    status_reg = SPI.transfer(0x0);
    digitalWrite(SLAVESELECT, HIGH);
    if ((status_reg & 0x02) == 0) {
      Serial.println("FAIL: write enable failed");
      once = 0;
      return;
    }

    digitalWrite(SLAVESELECT, LOW);
    SPI.transfer(SECTOR_ERASE);  // Sector erase
    SPI.transfer(once / 256);
    SPI.transfer(0x00);
    SPI.transfer(0x00);
    digitalWrite(SLAVESELECT, HIGH);

    do {
      digitalWrite(SLAVESELECT, LOW);
      SPI.transfer(RDSR);
      status_reg = SPI.transfer(0x0);
      digitalWrite(SLAVESELECT, HIGH);
      Serial.print("Status reg: ");
      Serial.println(status_reg, HEX);
    } while ((status_reg & 0x1) == 1);
    Serial.println("Sector erase: finished");
  }

  Serial.print("Page program: ");
  Serial.println(once);
  digitalWrite(SLAVESELECT, LOW);
  SPI.transfer(WREN); // Write enable
  digitalWrite(SLAVESELECT, HIGH);

  digitalWrite(SLAVESELECT, LOW);
  SPI.transfer(RDSR);
  status_reg = SPI.transfer(0x0);
  digitalWrite(SLAVESELECT, HIGH);
  if ((status_reg & 0x02) == 0) {
    Serial.println("FAIL: write enable failed");
    once = 0;
    return;
  }

  digitalWrite(SLAVESELECT, LOW);
  SPI.transfer(WRITE);  // Page program
  SPI.transfer(once / 256);
  SPI.transfer(once % 256);
  SPI.transfer(0);
  for (int i = 0; i < 256; i++) {
    SPI.transfer(b[i]);
  }
  digitalWrite(SLAVESELECT, HIGH);

  do {
    digitalWrite(SLAVESELECT, LOW);
    SPI.transfer(RDSR);
    status_reg = SPI.transfer(0x0);
    digitalWrite(SLAVESELECT, HIGH);
    Serial.print("Status reg: ");
    Serial.println(status_reg, HEX);
  } while ((status_reg & 0x1) == 1);

  Serial.println("Page program: finished");

  once++;
}


