# Ticket Anywhere

A comprehensive ticket booking application built with React (frontend) and Django REST Framework (backend).

## Features

- User authentication and authorization
- Event management
- Ticket booking system
- Admin panel for event management
- Responsive UI with modern design

## Prerequisites

### For Both Windows and Linux:
- Node.js (version 18 or higher)
- Python (version 3.8 or higher)
- PostgreSQL database

### Windows Installation:
1. **Node.js**: Download and install from [nodejs.org](https://nodejs.org/)
2. **Python**: Download and install from [python.org](https://python.org/)
3. **PostgreSQL**: Download and install from [postgresql.org](https://postgresql.org/)

### Linux Installation:
1. **Node.js**:
   ```bash
   sudo apt update
   sudo apt install nodejs npm
   ```

2. **Python**:
   ```bash
   sudo apt install python3 python3-venv python3-pip
   ```

3. **PostgreSQL**:
   ```bash
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Khant26/Ticket-Anywhere.git
cd Ticket-Anywhere
```

### 2. Backend Setup

Navigate to the backend directory:
```bash
cd ticket-backend
```

#### Create Virtual Environment:

**Windows:**
```bash
python -m venv .ticket
.ticket\Scripts\activate
```

**Linux:**
```bash
python3 -m venv .ticket
source .ticket/bin/activate
```

#### Install Dependencies:
```bash
pip install -r requirements.txt
```

#### Database Setup:
1. Create a PostgreSQL database named `ticket`
2. Update the `.env` file with your database credentials:
   ```
   DB_NAME=ticket
   DB_USER=your_postgres_username
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

#### Run Migrations:
```bash
python manage.py migrate
```

#### Create Super Admin User:
To access the Django admin panel and manage the application:

**Windows:**
```bash
python manage.py createsuperuser
```

**Linux:**
```bash
python manage.py createsuperuser
```

Follow the prompts to enter email, name, and password for the super admin account.

#### Start Backend Server:
```bash
python manage.py runserver
```
The backend will run at `http://localhost:8000`

You can access the Django admin panel at `http://localhost:8000/admin/` using the super admin credentials.

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd ticket-frontend
```

#### Install Dependencies:
```bash
npm install
```

#### Start Development Server:
```bash
npm run dev
```
The frontend will run at `http://localhost:5173`

### 4. Admin Dashboard Setup

Open a new terminal and navigate to the admin dashboard directory:
```bash
cd ticket_admin_dashboard
```

#### Install Dependencies:
```bash
npm install
```

#### Start Development Server:
```bash
npm run dev
```
The admin dashboard will run at `http://localhost:5173` (or a different port if configured)

## Usage

1. Ensure both backend and frontend servers are running
2. Open your browser and go to `http://localhost:5173`
3. Register/Login to access the application
4. Browse events and book tickets

## API Documentation

The backend provides REST API endpoints for:
- User authentication (JWT)
- Event management
- Ticket booking
- Admin operations

Base API URL: `http://localhost:8000/api/`

## Project Structure

```
Ticket-Anywhere/
├── ticket-frontend/         # User-facing React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── ticket-backend/          # Django application
│   ├── ticketapp/
│   ├── ticketanywhere/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
├── ticket_admin_dashboard/  # Admin dashboard React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
└── README.md
```

## Technologies Used

### Frontend:
- React 18
- Vite
- Tailwind CSS
- React Router
- Axios
- React i18next (for internationalization)

### Backend:
- Django 5.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Django CORS Headers

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues, please open an issue on GitHub or contact the development team.