# CS50 Switch 💡🔧

CS50 Switch is a smart IoT-based light switch system designed to automate your waking-up experience. Created as a final project for Harvard's CS50x, this system uses an ESP32 microcontroller, a servo motor, and a web interface to physically turn on your light switch at a scheduled time.

This project simulates a commercial product concept that makes mornings easier by using light as a natural wake-up trigger — all powered by open-source code and a clean, responsive web platform.

---

## 🚀 Purpose

> **"Waking up shouldn’t be painful."**

CS50 Switch was built to **simulate a real-world product** that helps users wake up more naturally. Instead of loud alarms, the servo-controlled system flips your light switch on at a precise time, giving your body a chance to adjust to light and start the day smoothly.

---

## 🌟 Features

- ✅ ESP32 + Servo powered mechanical switch
- 🌐 Web-based control panel (Flask + HTML/CSS)
- ⏰ Set alarms from your browser
- 📜 View and delete existing alarms
- 🔐 User authentication system
- 📱 Fully responsive (mobile, tablet, desktop)
- 🧠 Designed with usability and realism in mind
- 🧩 Modular and expandable for other IoT features

---

## 🧠 Technologies Used

- **ESP32 (microcontroller)** with Arduino code
- **Flask** (Python web framework)
- **HTML5 + CSS3 + Jinja** templating
- **SQLite** (local database)
- **JavaScript** (for AJAX-based alarm/switch POST requests)
- **Bootstrap-like custom responsive styling**
- **NTP time sync** for accurate ESP32 alarms

---

# 🛠️ How to Run Locally

## 🧩 Requirements
- Python 3.10+
- Flask
- ESP32 board + servo motor + breadboard
- Arduino IDE

---
## 🔧 ESP32 Setup
1. Open `esp32_servo_alarm.ino` in **Arduino IDE**.
2. Update your Wi-Fi credentials (`SSID`, `PASSWORD`).
3. Upload to ESP32 using USB.
4. Note the IP address shown in **Serial Monitor**.
5. Update `ESP32_IP` in `app.py` accordingly.

---

## 🧪 Demo Screenshots
📸 *No photos available at this time.*

---

## 🧱 Future Improvements
- 🔔 Add sound-based alarm toggle  
- 📡 Deploy backend to a cloud host (e.g. Render, Railway)  
- 📲 Add PWA support (installable web app)  
- 🔐 Add password hashing and login rate limiting  
- 🔋 Battery/solar powered ESP32 for full wireless solution  

---

## 📚 License
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## 🙌 Acknowledgements
- CS50x Harvard  
- ESP32 Arduino Core  
- ABB Smart Switch Product Inspiration  
- YouTube Channel *mr.wwhostheboss* for project inspiration  

---

### ✨ Built with passion by **Daniel Cordoba Gomez**  
> *"Automation begins with the little things."*

## 💻 Backend Setup

```bash

├── backend/
│   ├── app.py                # Flask app
│   ├── init_db.py            # Initializes SQLite DB
│   ├── users.db              # SQLite user + alarm data
│   ├── static/
│   │   └── style.css         # Web styling
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── signup.html
│       ├── alarm.html
│       ├── alarms.html
│       ├── switch_control.html
│       ├── requirements.html
│       ├── how_it_works.html
│       └── specs.html
└── arduino/
    └── esp32_servo_alarm.ino # ESP32 Arduino code

    
