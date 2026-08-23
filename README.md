# Dayflow – Employee Management System

Dayflow is a modern, user-friendly employee management platform designed to simplify everyday HR and employee operations. The project provides a centralized workspace where employees can access important work-related information such as profiles, attendance, leave requests, and salary details.

## 🚀 Features

* **User Authentication**

  * Sign In and Sign Up interfaces
  * Employee ID and email-based registration
  * Password visibility toggle
  * Remember Me option
  * Role-based access for HR and Employees

* **Employee Dashboard**

  * Personalized employee welcome section
  * Automatic date display
  * Quick-access cards for important services
  * Employee profile management
  * Attendance overview
  * Leave request access
  * Salary and payroll information
  * Recent activity tracking

* **Responsive Design**

  * Desktop-friendly interface
  * Tablet and mobile responsive layouts
  * Clean and modern UI
  * Interactive hover and focus states

## 🛠️ Tech Stack

* **HTML5** – Page structure and semantic markup
* **CSS3** – Styling, layouts, responsive design, and animations
* **JavaScript** – Client-side interactions and dynamic functionality
* **REST API** – Prepared integration for authentication and account creation

## 📂 Project Structure

```text
Dayflow/
│
├── login.html
├── homepage.html
├── profile.html
├── attendence.html
├── leave.html
├── payroll.html
├── hr_home.html
└── README.md
```

> Additional pages are part of the planned employee and HR workflow and may be developed further as the project progresses.

## 🔐 Authentication

The authentication interface supports separate **HR/Admin** and **Employee** workflows. The frontend is structured to communicate with backend REST API endpoints for login and account creation.

Example endpoints:

```text
POST /api/login
POST /api/signup
```

The login interface also provides feedback for successful authentication and server connection errors.

## 📊 Employee Dashboard

The employee dashboard provides quick access to:

| Module         | Purpose                             |
| -------------- | ----------------------------------- |
| My Profile     | View personal and job information   |
| Attendance     | Check daily and weekly attendance   |
| Leave Requests | Apply for and track leave           |
| Salary Details | View payroll and salary information |

The dashboard also displays today's attendance status and recent employee activity.

## 🎨 UI & Design

Dayflow follows a clean, professional design approach using:

* Minimal and modern layouts
* Blue-based professional color palette
* Card-based dashboard components
* Clear typography and spacing
* Responsive grids
* Interactive buttons and form controls

The login page uses a split-screen layout with branding and authentication sections, while the dashboard uses a navigation bar, hero section, quick-access cards, and information panels.

## 🔮 Future Improvements

Planned improvements include:

* Backend integration
* Database connectivity
* Secure authentication and authorization
* HR/Admin dashboard
* Real-time attendance management
* Leave approval workflow
* Payroll management
* Employee profile editing
* Notifications
* Improved role-based access control

## 📌 Project Status

**Currently in development**

The frontend foundation and core employee workflow have been established. Backend, database, and additional HR functionality can be integrated as the project evolves.

## 👨‍💻 Author

Developed as a web development project focused on building a practical employee management system with a modern frontend architecture.

---

**Dayflow — Every workday, perfectly aligned.**
