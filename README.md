# Transport Management System

A comprehensive system for managing a transport company's operations, including cargo types, vehicles, drivers, and routes.

## Features

- Cargo Types Management
  - Add, edit, and delete cargo types
  - View cargo type details and statistics

- Vehicle Management
  - Track vehicle status (active/repair/inactive)
  - Assign vehicles to drivers
  - Monitor vehicle usage and maintenance

- Driver Management
  - Add and manage driver information
  - Track driver assignments and availability
  - View driver history and performance

- Route Management
  - Create and plan routes
  - Track route status and progress
  - Assign drivers and vehicles
  - Monitor cargo details

- Dashboard
  - Overview of active routes
  - Vehicle and driver status
  - Quick access to common actions
  - Real-time statistics

## Requirements

- Python 3.8+
- Flask
- SQLAlchemy
- Other dependencies (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd transport-management-system
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db upgrade
```

## Running the Application

1. Start the development server:
```bash
flask run
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
transport-management-system/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS)
│   ├── css/
│   └── js/
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── cargo_types.html
    ├── vehicles.html
    ├── drivers.html
    └── routes.html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 