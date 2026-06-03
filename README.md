# Order Management System (OMS)

A web-based Order Management System built using Flask and SQL for managing products, inventory, and customer orders through an intuitive dashboard.

## Features

- Product Management
  - Add, update, delete, and view products
  - Track product inventory

- Order Management
  - Create and manage customer orders
  - View order history and status

- Inventory Tracking
  - Monitor stock availability
  - Prevent inventory inconsistencies

- Database Integration
  - Store and retrieve data efficiently using SQL

- Responsive User Interface
  - Clean and user-friendly design

## Tech Stack

### Backend
- Python
- Flask

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQL

## Project Structure

```text
app/
config/
run.py
requirements.txt
schema.sql
seed.py
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/samayshrey-dev/flask-oms-project1.git
cd flask-oms-project1
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file using `.env.example`.

### 6. Initialize Database

```bash
python seed.py
```

### 7. Run the Application

```bash
python run.py
```

## Learning Outcomes

- Developed a full-stack web application using Flask
- Implemented database-driven CRUD operations
- Designed modular backend architecture
- Worked with SQL schema design and data management
- Learned Git and GitHub version control workflows

## Future Improvements

- User Authentication and Authorization
- Dashboard Analytics
- Role-Based Access Control
- Email Notifications
- REST API Integration

## Author

**Samayshrey Patnaik**

- GitHub: https://github.com/samayshrey-dev
- LinkedIn: [Your LinkedIn URL]
