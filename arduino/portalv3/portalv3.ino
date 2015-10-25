const int keymatic_open = 10;
const int keymatic_close = 16;
const int status_pin = 14;
const int beeper = 15;
const int closebutton = 9;
const int doorcontact = 8;
const int reedcontact = 7;
int closing_requested = 0;

void setup()
{
  Serial.begin(9600);
  
  pinMode(keymatic_open, OUTPUT);
  pinMode(keymatic_close, OUTPUT);
  pinMode(status_pin, OUTPUT);
  pinMode(beeper, OUTPUT);
  pinMode(closebutton, INPUT);
  pinMode(doorcontact, INPUT);
  pinMode(reedcontact, INPUT);
  
}

void loop()
{
  int comm1 = Serial.parseInt();
  int comm2 = Serial.parseInt();
  if(Serial.read() == '\n')
  {
    parseCMD(comm1, comm2);
  }
  if(digitalRead(closebutton))
  {
    closing_requested = 1;
  }
}

void parseCMD(int comm1, int comm2)
{
  switch(comm1)
  {
    case 1:
      switch(comm2)
      {
        case 0:
          digitalWrite(keymatic_open, LOW);
          Serial.println('0');
          break;
        case 1:
          digitalWrite(keymatic_open, HIGH);
          Serial.println('1');
          break;
      }
      break;
    case 2:
      switch(comm2)
      {
        case 0:
          digitalWrite(keymatic_close, LOW);
          Serial.println('0');
          break;
        case 1:
          digitalWrite(keymatic_close, HIGH);
          Serial.println('1');
          break;
      }
      break;
  
    case 3:
      switch(comm2)
      {
        case 0:
          digitalWrite(status_pin, LOW);
          Serial.println('0');
          break;
        case 1:
          digitalWrite(status_pin, HIGH);
          Serial.println('1');
          break;
      }
      break;
    case 4:
      switch(comm2)
      {
        case 0:
          digitalWrite(beeper, LOW);
          Serial.println('0');
          break;
        case 1:
          digitalWrite(beeper, HIGH);
          Serial.println('1');
          break;
      }
      break;
      
    case 10:
      Serial.println(digitalRead(closebutton));
      break;
    case 11:
      Serial.println(digitalRead(doorcontact));
      break;
    case 12:
      Serial.println(digitalRead(reedcontact));
      break;
    case 20:
      switch(comm2)
      {
        case 0:
          Serial.println(closing_requested);
          break;
        case 1:
          closing_requested = 0;
          break;
      }
      break;
  }
}
          
        
