#include <Stepper.h>

#define OFF 0xFF

// for the DC motor
#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN2 6
#define IN1 7

int pos = 0;
long prevT = 0;
float eprev = 0;
float eintegral = 0;

// for the arms
#define openARM 0x0F
#define closeARM 0x1F

const short int armOP   = 8;
const short int armCL   = 9;

// for the turning

const int stepsPerRevolution = 64;
Stepper myStepper(stepsPerRevolution, 22, 24, 26, 28);

void setup() {

  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(armOP, OUTPUT);          //Sets that pin as an output
  pinMode(armCL, OUTPUT);
  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA), readEncoder, RISING);

  // set the speed at 60 rpm:
  myStepper.setSpeed(400);
}

void loop() {  
  float motor_change  = Serial.parseFloat();
  float arm_movement = Serial.parseFloat();
  float steer_move =  Serial.parseFloat();
  Serial.println(motor_change);
  Serial.println(arm_movement);
  Serial.println(steer_move);
  if (motor_change) {
    // set target position
    int target = motor_change;
    // PID constants
    float kp = 1.2;
    float kd = 0.3;
    float ki = 0.001;

    // time difference
    long currT = micros();
    float deltaT = ((float) (currT - prevT)) / ( 1.0e6 );
    prevT = currT;

    // error
    int e = pos - target;

    // derivative
    float dedt = (e - eprev) / (deltaT);

    // integral
    eintegral = eintegral + e * deltaT;

    // control signal
    float u = kp * e + kd * dedt + ki * eintegral;

    // motor power
    float pwr = fabs(u);
    if ( pwr > 255 ) {
      pwr = 255;
    }

    // motor direction
    int dir = 1;
    if (u < 0) {
      dir = -1;
    }

    // signal the motor
    setMotor(dir, pwr, PWM, IN1, IN2);

    // store previous error
    eprev = e;
    delay(3);
    motor_change = 0;

  }
  if (arm_movement)
  {
    if (arm_movement == openARM) {
      digitalWrite(armOP, HIGH);
      digitalWrite(armCL, LOW);
    }
    else if (arm_movement == closeARM) {
      digitalWrite(armOP, LOW);
      digitalWrite(armCL, HIGH);
    }
    else {
      digitalWrite(armOP, LOW);
      digitalWrite(armCL, LOW);
    }
    delay(3);
    arm_movement = 0;
  }

  steer_move = 320;

  if (steer_move) {
    myStepper.step(steer_move / 5.625);
    delay(3);
    steer_move = 0;
  }

}


void setMotor(int dir, int pwmVal, int pwm, int in1, int in2) {
  analogWrite(pwm, pwmVal);
  if (dir == 1) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else if (dir == -1) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
}

void readEncoder() {
  int b = digitalRead(ENCB);
  if (b > 0) {
    pos++;
  }
  else {
    pos--;
  }
}
