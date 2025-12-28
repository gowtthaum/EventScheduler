# 📅 Event Scheduler & Resource Allocation System

A web-based application built using **Flask** that allows users to manage events, resources, and allocate resources efficiently within event timelines.  
This project is designed to avoid resource conflicts and ensure proper scheduling with a clean dashboard interface.

---

## 🚀 Features

### ✅ Event Management
- Create events with title, start date & time, and end date & time
- Edit and delete events
- View all events in a structured list

### ✅ Resource Management
- Add and manage resources (e.g., Conference Hall, Projector, Sound System)
- Resources can be reused across multiple events (if time permits)

### ✅ Resource Allocation
- Allocate resources to events **within the event time duration**
- Prevents overlapping allocation of the same resource
- Displays allocated resources clearly with:
  - Event name
  - Resource name
  - Date
  - Time
  - Day

### ✅ Dashboard
- Overview of:
  - Total events
  - Total resources
  - Total allocations
- Clean sidebar navigation for easy access

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS (Custom styling)
- **Templating Engine:** Jinja2
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

event-scheduler/
│
├── app/
│ ├── routes/
│ │ ├── events.py
│ │ ├── resources.py
│ │ └── allocations.py
│ ├── models.py
│ ├── templates/
│ │ ├── layout.html
│ │ ├── dashboard.html
│ │ ├── events/
│ │ ├── resources/
│ │ └── allocations/
│ └── static/
│ └── css/style.css
│
├── migrations/
├── instance/
├── config.py
├── run.py
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/event-scheduler.git
cd event-scheduler
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
Activate:

Windows:

bash
Copy code
venv\Scripts\activate
Mac/Linux:

bash
Copy code
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Application
bash
Copy code
python run.py
Open browser:

cpp
Copy code
http://127.0.0.1:5000
📊 How Resource Allocation Works
Resources are allocated only within the event duration

If a resource is already allocated for the same time, it cannot be reused

Ensures efficient planning and avoids conflicts

🎯 Use Cases
College event management

Conference scheduling

Office meeting & resource planning

Project demonstrations

🧑‍💻 Author
Gowtham
Final Year Project – Event Scheduling System
Built with ❤️ using Flask

📌 Future Enhancements
Calendar view for events

Resource utilization reports

User authentication (Admin / User)

Email notifications

