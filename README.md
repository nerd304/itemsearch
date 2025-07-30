# ItemVerse: Item Catalog Application

This is a database-driven web application built in Python for managing a catalog of items. It provides full CRUD (Create, Read, Update, Delete) functionality, live search, and bulk import capabilities.

**Core Technology Stack:**
*   **Backend Framework:** Python with Flask
*   **Database:** SQLite with SQLAlchemy
*   **Templating:** Jinja2
*   **Styling:** Tailwind CSS

---

## How to Run in a Development Environment

This project is configured to run in a Nix-based environment like the one provided by Firebase Studio or Gitpod.

1.  **Activate Environment & Install Dependencies:** The environment should automatically create a Python virtual environment at `.venv` and install the necessary packages from `requirements.txt` and `package.json`. If you need to do it manually, run:
    ```bash
    source .venv/bin/activate
    pip install -r requirements.txt
    npm install
    ```

2.  **Run the Development Server:** Use the provided `devserver.sh` script. This script handles building the CSS with Tailwind and running the Flask development server. In an environment like Firebase Studio, you can simply run the `web` preview task.
    ```bash
    ./devserver.sh
    ```

---

## How to Host on a Production Server

To host this application yourself, you need to move from the development setup to a more robust production setup. The following guide explains how to deploy on a typical Linux server (e.g., Ubuntu).

### 1. Install System Dependencies

First, you need to install Python, `pip`, `git`, Nginx (our web server), and the Node.js environment (for building CSS).

```bash
# Update package list
sudo apt update

# Install system packages
sudo apt install python3 python3-pip python3-venv git nginx nodejs npm
```

### 2. Get Your Project Code

Clone your project from your Git repository onto the server.

```bash
# Clone your project
git clone https://github.com/nerd304/itemsearch.git
cd itemsearch
```

### 3. Set Up the Application

Prepare your application files and dependencies.

1.  **Add Gunicorn to your dependencies.** Gunicorn is a production-grade WSGI server that will run your Flask app. Add it to your `requirements.txt` file.
    ```
    # requirements.txt
    flask
    Flask-SQLAlchemy
    gunicorn  # <-- Add this line
    ```
2.  **Create a Python Virtual Environment**
    ```bash
    # Create the virtual environment
    python3 -m venv .venv

    # Activate it
    source .venv/bin/activate

    # Install Python packages
    pip install -r requirements.txt
    ```
3.  **Build the CSS for Production**
    ```bash
    # Install Node.js dependencies
    npm install

    # Run the one-time production build for your CSS
    npm run build:css
    ```

### 4. Configure Nginx as a Reverse Proxy

Nginx will be the public-facing web server. It will handle incoming web traffic and pass requests to our Gunicorn application.

1.  **Create an Nginx configuration file for your site.**
    ```bash
    sudo nano /etc/nginx/sites-available/itemsearch
    ```
2.  **Paste the following configuration into the file.** Make sure to replace `your_domain_or_ip` with your server's actual domain or IP address.
    ```nginx
    server {
        listen 80;
        server_name your_domain_or_ip;

        location /static {
            alias /path/to/your/itemsearch/project/static;
        }

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```
3.  **Enable the site and restart Nginx.**
    ```bash
    # Link the config file to enable it
    sudo ln -s /etc/nginx/sites-available/itemsearch /etc/nginx/sites-enabled/

    # Test the Nginx configuration for errors
    sudo nginx -t

    # Restart Nginx to apply the changes
    sudo systemctl restart nginx
    ```

### 5. Run the Application as a Service

To ensure your app runs continuously and restarts automatically, run Gunicorn as a `systemd` service.

1.  **Create a service file.**
    ```bash
    sudo nano /etc/systemd/system/itemsearch.service
    ```
2.  **Paste the following configuration.** Replace the paths and `User` with the correct values for your project and system.
    ```ini
    [Unit]
    Description=Gunicorn instance to serve itemsearch
    After=network.target

    [Service]
    User=your_username # The user you are logged in as
    Group=www-data
    WorkingDirectory=/path/to/your/itemsearch/project
    Environment="PATH=/path/to/your/itemsearch/project/.venv/bin"
    ExecStart=/path/to/your/itemsearch/project/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 main:app

    [Install]
    WantedBy=multi-user.target
    ```
3.  **Start and enable the service.**
    ```bash
    # Start the service now
    sudo systemctl start itemsearch

    # Enable the service to start automatically on server boot
    sudo systemctl enable itemsearch
    ```

Your application should now be live and accessible from your server's IP address or domain name.
