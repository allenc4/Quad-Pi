#include <pigpio.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <time.h>


#define DEBUG_PRINT 1
#define TRUE 1


const int SERVO_GPIO = 18;    // GPIO number of the attached servo
const double PULSE_CONST = 10.588;   // 10.588 PWM per 1 degree
int cur_pulse = 0;
int cur_angle = 0;

double distance = 0.00;

const int CENTER_PULSE     = 1550; //PWM for servo center/middle
const int ANGLE_MOVEMENT   = 45;   //Number of degrees to rotate left+right of center
const int ANGLE_CHANGE     = 2;    //Move servo x degrees each pulse

int degree_change;
int max_left;
int max_right; 

// Structure for sleeping 
struct timespec sleepTime;

// Function Prototypes
void finish();
void set_servo();
void debug_print(char* message);

int main()
{
    // Take integer only values
    degree_change = (int) round(ANGLE_CHANGE * PULSE_CONST);
    // Max PWM for left and right
    max_left  = (int) round(CENTER_PULSE - (ANGLE_MOVEMENT * PULSE_CONST));
    max_right = (int) round(CENTER_PULSE + (ANGLE_MOVEMENT * PULSE_CONST));

    sleepTime.tv_sec = 0;
    sleepTime.tv_nsec = 5000000;

    // Start the pigpio library
    int connected = gpioInitialise();
    if (connected == PI_INIT_FAILED)
    {
        printf("Error initializing GPIO librariesi\n");
        exit(-1);
    }

    printf("Connected to servo\n");

    cur_pulse = max_left;
    cur_angle = (int) round((cur_pulse / PULSE_CONST) - (CENTER_PULSE / PULSE_CONST));

    signal(SIGINT, finish);
    
    // Start the servo at the left
    set_servo(max_left);
    
    while (TRUE)
    {
        // Servo position all the way to the left, start moving right
        while (cur_pulse < max_right)
        {
            cur_pulse = cur_pulse + degree_change;
            cur_angle = cur_angle + ANGLE_CHANGE;
            set_servo(cur_pulse);
        }

        // Servo all the way to the right, start moving left
        while (cur_pulse > max_left)
        {
            cur_pulse = cur_pulse - degree_change;
            cur_angle = cur_angle - ANGLE_CHANGE;
            set_servo(cur_pulse);
        }
    }

    
    return 0;
}

void set_servo(int pulse)
{
    //Ensure the pulse is a whole number
    int servoPulse = gpioServo(SERVO_GPIO, pulse);
    //distance = lidar.getDistance();
#ifdef DEBUG_PRINT
    printf("Servo angle: %d, pulse: %d\n", cur_angle, pulse);
    //printf("Lidar distance: %d\n, distance);
#endif
    nanosleep(&sleepTime, NULL);
}

void finish()
{
    // Switch servo off
    set_servo(0);
    gpioTerminate();
    exit(0);
}

void debug_print(char* message)
{
#ifdef DEBUG_PRINT
    printf("%s\n", message);
#endif
}

