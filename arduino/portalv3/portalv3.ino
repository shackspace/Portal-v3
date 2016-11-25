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
  pinMode(closebutton, INPUT_PULLUP);
  pinMode(doorcontact, INPUT_PULLUP);
  pinMode(reedcontact, INPUT_PULLUP);
  
}

unsigned long target_timeout;  // target for timeouts
int button_state = 0;       // 0 = idle, button not pushed
                            // 1 = checking, check if button is pushed, check if it was just a random signal or intended
                            // 2 = closing, wait for raspi to read button state or until the timeout is reached
                            // 3 = wait, wait until the button is released

void loop()
{
  if(Serial.available() > 0)
  {
    int comm1 = Serial.parseInt();
    int comm2 = Serial.parseInt();
    if(Serial.read() == '\n')
    {
      parseCMD(comm1, comm2);
    }
  }

  switch(button_state)
  {
    case 0:   // idle
      closing_requested = 0;
      if(!digitalRead(closebutton)) // button pushed
      {
        target_timeout = millis() + 100;  // set target 100 milliseconds into the future
        button_state = 1;
      }
      break;
    case 1:   // checking
      if(digitalRead(closebutton))  // button_released
      {
        button_state = 0;   // return to idle
      }
      else
      {
        if(check_timer())   // timeout reached
        {
          target_timeout = millis() + 10000; // set target 10 seconds into the future
          closing_requested = 1;
          button_state = 2; // start closing
        }
      }
      break;
    case 2:   // closing
      if(closing_requested == 0)  // the request was read by the raspi
      {
        button_state = 4;   // start waiting
      }
      else
      {
        if(check_timer())   // timed out waiting for the raspi. clear request flag and go to idle
        {
          closing_requested = 0;
          button_state = 0;
        }
      }
      break;
    case 4:   // wait
      if(digitalRead(closebutton))  // button is released
      {
        button_state = 0;
      }
      break;
  }

  
}

bool check_timer()
{
  if(millis() >= target_timeout)  // current time is greater than the target time
  {
    if(target_timeout < 1000000)  // the target time is smaller than 1000 seconds
    {
      if(millis() < 2000000)      // if the current time is smaller than 2000 seconds we can be sure it's not greater than the target because the target overflow but because it really is
      {
        return true;
      }
    }
    else  // no need to check for overflow problems
    {
      return true;
    }
  }
  return false;
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
          Serial.println("1 0");
          break;
        case 1:
          digitalWrite(keymatic_open, HIGH);
          Serial.println("1 1");
          break;
      }
      break;
    case 2:
      switch(comm2)
      {
        case 0:
          digitalWrite(keymatic_close, LOW);
          Serial.println("2 0");
          break;
        case 1:
          digitalWrite(keymatic_close, HIGH);
          Serial.println("2 1");
          break;
      }
      break;
  
    case 3:
      switch(comm2)
      {
        case 0:
          digitalWrite(status_pin, LOW);
          Serial.println("3 0");
          break;
        case 1:
          digitalWrite(status_pin, HIGH);
          Serial.println("3 1");
          break;
      }
      break;
    case 4:
      switch(comm2)
      {
        case 0:
          digitalWrite(beeper, LOW);
          Serial.println("4 0");
          break;
        case 1:
          digitalWrite(beeper, HIGH);
          Serial.println("4 1");
          break;
      }
      break;
      
    case 10:
      Serial.println("10 " + String(digitalRead(closebutton)));
      break;
    case 11:
      Serial.println("11 " + String(digitalRead(doorcontact)));
      break;
    case 12:
      Serial.println("12 " + String(digitalRead(reedcontact)));
      break;
    case 20:
      switch(comm2)
      {
        case 0:
          Serial.println("20 " +  String(closing_requested));
          break;
        case 1:
          closing_requested = 0;
          Serial.println("20 " +  String(closing_requested));
          break;
      }
      break;
  }
}
          
        
