+++
title = “Solar-Clock Device Design Conversation”
date = “2025-12-10T10:00:00-05:00”
draft = false
categories = [“electronics”]
tags = [“arduino”,“rtc”,“equation-of-time”,“solar-tracking”,“design”]
+++

Full Conversation Log

User:
I want to design a device that has a real time clock and will automaticaly correct itself by way of an array of 12 photo sensors arrange such that they are aranged in an arc pointed at the southern sky (in the northern hemisphere) that will detect the suns transition across the sky and note it’s position as to adjust the clock at 6 pm using the gathered data and equation of time taking into affect the devices latitude, logitude and elevations and atmospheric refraction

Assistant:
That sounds like an interesting project! Designing a device that utilizes an array of photo sensors to detect the sun’s position and correct a real-time clock accordingly involves several steps. Here’s a basic outline of how you might approach it:
	1.	Hardware Design: … (overview of components and steps)
	2.	Sensor Calibration: …
	3.	Data Collection: …
	4.	Position Calculation: …
	5.	Clock Adjustment: …
	6.	Testing and Refinement: …
	7.	User Interface (Optional): …
	8.	Enclosure and Final Assembly: …

(Assistant gave a general outline and suggestions on libraries and testing.)

⸻

User:
Let’s assume the device has no external access to the Network time protocol. Let’s also assume it can adjust itself if it only has the year month and day entered and a rough estimate of the time at its starting point

Assistant:
Without access to an external time source like NTP, the device would rely solely on its internal mechanism for timekeeping and adjustment. Here’s how you could refine the approach:
(Assistant outlined initial calibration, sun tracking, clock adjustment, iterative refinement, fallback, UI, and power.)

⸻

User:
The device will have a Real Time Clock or RTC module

Assistant:
Incorporating an RTC module simplifies the timekeeping. Steps were refined to include RTC:
	•	initial setup w/ user-entered location and date, RTC initialization
	•	sun position tracking with photo sensors
	•	data collection and storing
	•	daily adjustment at a set time using collected data + EOT + lat/lon/elevation/refraction
	•	RTC adjustment and iterative refinement
	•	fallback mechanism and UI/power management

⸻

User:
Using an Arduino a RTC, a 12 volt battery, array of 12 photo sensors, what would my circut look like and what is the arduino code necessary to fulfill the entire functionality of this device

Assistant:
Provided a basic circuit ASCII diagram and component list, and gave a starter Arduino sketch with RTC library usage. Key points included:
	•	RTC (e.g., DS3231) on I2C (SDA/A4, SCL/A5 on Uno)
	•	photo sensors mapped to digital pins (example pins 2–13) — note: analog photodiodes/photocells usually wired to analog inputs via voltage dividers for reading light intensity, not digital pins.
	•	power from 12V battery (with regulator for Arduino 5V/3.3V)
	•	starter code to read RTC and sensors, store sensor values, and a placeholder to run adjustment at 18:00.

(Assistant provided initial sketch and reminded to install RTClib, and implement sun-position algorithm later.)

⸻

User:
Also add a segmented display and switches to the circuit and code to allow for date, time and location entry and update code to reflect the data entry. Also give detailed pin level connectivity for the circuit and code.

Assistant:
Updated the design: suggested adding a 7-segment display and switches, wiring suggestions, and updated code skeleton:
	•	segmentPins[] mapped to digital outputs (example)
	•	switchPins[] mapped to digital inputs with INPUT_PULLUP
	•	RTC initialization remains on I2C
	•	prompt to implement input handling, debouncing, and display formatting
	•	still left many implementation details (specific pin numbers, current-limiting resistors, multiplexing or driver for display if multi-digit, or using a display driver like TM1637 or MAX7219).

⸻

User:
I do not see where the code is implementing the equation of time or EOT to calculate the actual time or how the photo sensor data is used in that calcuation

Assistant:
Acknowledged oversight. Proposed how to integrate EOT and sensor data:
	•	add calculateEOT(year, month, day) function
	•	collect sun position data throughout day from sensor array (store azimuth estimates)
	•	at 6 pm, compute EOT, compare observed solar transit/azimuth to expected solar position (which requires latitude/longitude/elevation and solar position algorithm), compute time offset, and adjust RTC via rtc.adjust(...).
(Assistant provided function prototypes and integration point in main loop.)

⸻

User:
write the code for the calculateEOT function

Assistant:
Provided a simplified C++ implementation for an Arduino sketch:

```cpp
float calculateEOT(int year, int month, int day) {
    float n = 367 * year - 7 * (year + (month + 9) / 12) / 4 + 275 * month / 9 + day - 730531.5;
    float L = 280.461 + 0.9856474 * n;

    // Convert L to degrees (0 to 360)
    L = fmod(L, 360);
    if (L < 0) {
        L += 360;
    }

    // Convert L to radians
    float L_rad = L * PI / 180;

    // Calculate the Equation of Time (in minutes)
    float E = 229.18 * (0.000075 + 0.001868 * cos(L_rad) - 0.032077 * sin(L_rad) - 0.014615 * cos(2 * L_rad) - 0.040849 * sin(2 * L_rad));

    // Convert EOT to hours
    float EOT_hours = E / 60;

    return EOT_hours;
}
```

Notes given: include <math.h>, this is a simplified approximation — other, more accurate EOT formulas use the solar mean anomaly, true longitude, obliquity, etc. The assistant recommended verifying against authoritative sources for high accuracy.

