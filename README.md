CS50 Final Project Video: https://youtu.be/YIzKUIyuuo4

# CS50 Switch: An Intelligent Alarm-Controlled Light Activation System

**Author:** Daniel Córdoba Gómez
**Course:** CS50x (Harvard University)
**Project Type:** Final Project

---

## Introduction

This project, titled **CS50 Switch**, is a complete home automation system designed to activate a traditional light switch automatically through scheduled alarms, using a web interface connected to a microcontroller (ESP32) and a servo motor. The purpose behind this project was to design a system that wakes users up in a natural and consistent way by turning on the lights automatically at a specific time. Instead of relying on sound alarms, which are often jarring and unpleasant, CS50 Switch leverages physical light activation to create a calmer, healthier waking experience.

The system includes a responsive web application with login capabilities, a backend powered by Flask and SQLite, and an embedded control unit (ESP32) that communicates with the frontend to carry out tasks in the physical world. The servo motor physically actuates a mechanical light switch, effectively turning on or off any connected room light.

This README serves to comprehensively document the purpose, structure, components, and development choices of the project, along with notes on hardware-software integration and user interface design.

---

## Motivation

While many smart light systems exist, they often require the installation of smart bulbs or complex circuitry that replaces traditional infrastructure. I wanted to create something more **practical and universally adaptable** — a retrofit solution that does not require changing existing light switches or altering a home’s wiring.

The idea came from a simple problem: how can one wake up peacefully without the harshness of a sound alarm? I believed light-based awakening could solve this. Instead of designing a new light bulb, I decided to automate the existing light switch using accessible hardware (ESP32, servo, and 3D-printed components).

---

## Functionality Overview

The CS50 Switch system supports the following core functionalities:

* **Alarm Management:** Users can set daily repeating alarms via a web form.
* **Physical Control:** A servo motor is connected to a mechanical switch to simulate a press.
* **Manual Control:** Lights can also be turned on/off manually from the web interface.
* **User Accounts:** Secure sign-up and login system for personalized experience.
* **Persistent Storage:** Alarms are stored in a database and associated with individual users.
* **NTP Synchronization:** ESP32 fetches accurate time using NTP with time zone support (CET).
* **Daily Reset:** Alarms trigger only once per day, then reset automatically.

---

## File and Component Descriptions

### Web Application (Flask)

* **`app.py`**

  * Main Flask server handling all HTTP routes.
  * Manages user sessions, alarm CRUD operations, and ESP32 communication.
  * Uses decorators for route protection and user management.

* **`init_db.py`**

  * Initializes the SQLite database with tables for `users` and `alarms`.

* **`users.db`**

  * SQLite database file storing registered user credentials and their alarms.

* **Templates (`templates/` folder)**

  * `base.html`: Base layout including header, navigation, and global structure.
  * `login.html` / `signup.html`: Forms for authentication.
  * `home.html`: Homepage overview of system functionality.
  * `alarm.html`: Alarm scheduling form.
  * `alarms.html`: Alarm listing with delete functionality.
  * `specs.html`, `how_it_works.html`, `requirements.html`, `switch_control.html`: Additional pages for system education and use.

* **Static Files (`static/`)**

  * `style.css`: Stylesheet for layout, colors, and responsive design.

### Embedded System (ESP32)

* **`esp32_alarm.ino`**

  * Written in C++ using Arduino framework.
  * Connects to Wi-Fi, syncs time via NTP, and exposes `/alarm` and `/control` POST endpoints.
  * Controls servo motor to physically press the switch at alarm time.
  * Time is reset every boot to ensure accuracy.
  * Time zone is configured for Spain (CET/CEST).

### Hardware Components

* ESP32 Dev Board (NodeMCU)
* SG90 Servo Motor (connected to GPIO 13)
* Breadboard with 5V power rails
* Physical wall light switch
* Custom 3D-printed bracket to hold the servo in position
* Power adapter (USB)

---

## Design Decisions and Justifications

### Why ESP32?

The ESP32 was selected for its Wi-Fi capabilities, real-time clock support, and low cost. It allows reliable time synchronization and has the processing power required to manage web endpoints.

### Why SQLite?

Given the lightweight nature of the application and single-user access pattern, SQLite was more than sufficient. It also provides fast development and easy portability.

### Alarm Repetition Logic

Originally, alarms were designed to execute only once. But for practical use, especially as a wake-up system, it made more sense to have **daily repeating alarms**. This required a redesign of the flag logic to prevent repeated triggering within the same minute, while resetting the `alarmTriggered` state afterward.

### HTML + JS Simplicity

Rather than using React or any front-end framework, I kept the project in vanilla HTML/JS to maintain clarity and simplicity, especially since the UI is minimal and focused.

### Light Activation via Servo

Many smart home projects use relays or smart bulbs. I intentionally avoided this route to make CS50 Switch compatible with **any existing physical light switch**, regardless of age or manufacturer.

---

## Challenges

* **Time Zone Configuration:** The ESP32 originally reported the wrong time due to incorrect `configTime()` parameters. The issue was resolved by specifying timezone rules using `configTzTime("CET-1CEST,M3.5.0/2,M10.5.0/3", ...)`.

* **Network Reliability:** Because the ESP32 is hosted on a local IP, communication from external networks can fail. Ideally, a local DNS or cloud-based relay would improve reliability.

* **Physical Alignment:** Ensuring the servo accurately presses the light switch required iterative 3D printing and testing.

* **State Management:** Preventing the alarm from re-triggering within the same minute required careful timing logic.

---

## Future Improvements

* Add multi-day alarm scheduling and optional weekday filters.
* Use a real-time clock (RTC) module for redundancy in case of no Wi-Fi.
* Integrate an OLED or touchscreen on ESP32 for local UI control.
* Deploy server on Raspberry Pi for local hosting without needing a cloud backend.
* Add voice assistant integration (Google Assistant, Alexa).

---

## Conclusion

CS50 Switch is a fully functional IoT system designed for simplicity, reliability, and compatibility with everyday environments. It bridges web development with embedded systems and real-world physical interaction in a meaningful and accessible way. The project represents a culmination of skills developed through the CS50 course and goes beyond the minimal requirements by combining mechanical design, software development, and human-centered interaction.

The end product is not just a technical project, but a useful, real-world solution to a common problem: waking up better.

---

**Thank you for reviewing my final project.**

```
```

    
