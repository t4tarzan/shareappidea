# Student Startup Ideas Platform

A simple, modern web application for students to submit and showcase their startup ideas. Built with Python Flask and SQLite, designed to be easy to deploy and use.

## Features

- Submit startup ideas with title, description, and problem statement
- View all ideas in a responsive grid layout
- Simple and intuitive user interface
- Mobile-friendly design
- No external database required (uses SQLite)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
python run.py
```

Then open your browser and go to `http://localhost:5000`

### Creating a Standalone Executable

1. Install PyInstaller if you haven't already:
```bash
pip install pyinstaller
```

2. Create the executable:
```bash
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" run.py
```

3. The executable will be created in the `dist` directory

## Project Structure

```
student-startup-ideas/
├── app/                 # Application package
│   ├── __init__.py     # Application factory
│   ├── models.py       # Database models
│   └── routes.py       # Application routes
├── instance/           # Instance folder (created at runtime)
│   └── startup_ideas.db  # SQLite database
├── static/             # Static files
│   ├── css/           
│   │   └── style.css  
│   └── js/
│       └── main.js    
├── templates/          # HTML templates
│   ├── base.html      
│   ├── index.html     
│   └── submit.html    
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

## Customization

### Changing the Theme

You can customize the colors by modifying the CSS variables in `static/css/style.css`:

```css
:root {
    --primary: #2563eb;      /* Primary brand color */
    --primary-hover: #1d4ed8; /* Primary hover state */
    --text: #1f2937;         /* Main text color */
    --bg: #f9fafb;           /* Background color */
    --card-bg: #ffffff;      /* Card background */
}
```

### Adding New Categories

To add or modify categories, edit the `select` element in `templates/submit.html`:

```html
<select id="category" name="category">
    <option value="">Select a category</option>
    <option value="Technology">Technology</option>
    <!-- Add more categories here -->
</select>
```

## License

This project is open source and available under the [MIT License](LICENSE).
