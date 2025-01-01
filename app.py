import requests
import os
import json
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

app_name = "National Rail Data Downloader"
version = '1.0.0'

# Config file path
CONFIG_FILE = os.path.expanduser(f"~/Documents/{app_name}/config.json")

# Default settings
DEFAULT_CONFIG = {
    "username": "",
    "password": "",
    "save_location": os.path.expanduser("~/Downloads")
}

# Report URLs
REPORT_URLS = {
    "Fares": "https://opendata.nationalrail.co.uk/api/staticfeeds/2.0/fares",
    "Routeing Guide": "https://opendata.nationalrail.co.uk/api/staticfeeds/2.0/routeing",
    "Timetable": "https://opendata.nationalrail.co.uk/api/staticfeeds/3.0/timetable",
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r") as config_file:
        return json.load(config_file)

def save_config(config):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=4)

# Prompt user to set missing credentials if not set
def prompt_for_credentials():
    config = load_config()
    changed = False

    if not config["username"]:
        config["username"] = tk.simpledialog.askstring("Input", "Enter Username:")
        changed = True
    if not config["password"]:
        config["password"] = tk.simpledialog.askstring("Input", "Enter Password:", show="*")
        changed = True

    if changed:
        save_config(config)

def authenticate(config):
    token_url = "https://opendata.nationalrail.co.uk/authenticate"
    token_headers = {'Content-Type': 'application/json'}
    token_payload = {'username': config["username"], 'password': config["password"]}
    
    response = requests.post(token_url, json=token_payload, headers=token_headers)
    response.raise_for_status()
    return response.json().get('token')

def download_report(report_name):
    config = load_config()
    if not config["username"] or not config["password"]:
        messagebox.showerror("Error", "Username and password are not set. Please update your settings.")
        return

    try:
        auth_token = authenticate(config)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Authentication failed: {str(e)}")
        return

    data_url = REPORT_URLS[report_name]
    data_headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'X-Auth-Token': auth_token,
    }

    try:
        response = requests.get(data_url, headers=data_headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to download data: {str(e)}")
        return

    zip_file_path = os.path.join(config["save_location"], f"{report_name.lower().replace(' ', '_')}.zip")

    try:
        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(response.content)
        messagebox.showinfo("Success", f"{report_name} file saved to: {zip_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def update_save_location_callback(settings_labels):
    config = load_config()
    save_location = filedialog.askdirectory(title="Select Save Location")
    if save_location:
        config["save_location"] = save_location
        save_config(config)
        messagebox.showinfo("Success", "Save location updated successfully.")
        refresh_settings_labels(settings_labels)

def update_username_callback(settings_labels):
    config = load_config()
    username = tk.simpledialog.askstring("Input", "Enter Username:", initialvalue=config.get("username", ""))
    if username is not None:  # Allow clearing if user wants
        config["username"] = username
        save_config(config)
        messagebox.showinfo("Success", "Username updated successfully.")
        refresh_settings_labels(settings_labels)

def update_password_callback(settings_labels):
    config = load_config()
    password = tk.simpledialog.askstring("Input", "Enter Password:", show="*", initialvalue=config.get("password", ""))
    if password is not None:  # Allow clearing if user wants
        config["password"] = password
        save_config(config)
        messagebox.showinfo("Success", "Password updated successfully.")
        refresh_settings_labels(settings_labels)

def refresh_settings_labels(labels):
    # labels is a dict: {'username': ..., 'password': ..., 'location': ...}
    config = load_config()
    username = config["username"] if config["username"] else "Not set"
    password = config["password"]
    password_masked = '*' * len(password) if password else "Not set"
    save_location = config["save_location"] if config["save_location"] else "Not set"

    labels["username"].config(text=f"Username: {username}")
    labels["password"].config(text=f"Password: {password_masked}")
    labels["location"].config(text=f"Save Location: {save_location}")

def main():
    # Ensure credentials are set on first run
    prompt_for_credentials()

    root = tk.Tk()
    root.title(app_name)
    root.geometry("500x300")

    tab_control = ttk.Notebook(root)

    # Download Tab
    download_tab = ttk.Frame(tab_control)
    tab_control.add(download_tab, text="Download Data")
    tk.Label(download_tab, text=app_name, font=("Helvetica", 16)).pack(pady=20)
    tk.Label(download_tab, text="Choose a report to download:", font=("Helvetica", 12)).pack(pady=10)

    # Individual Download Buttons
    tk.Button(download_tab, text="Download Fares", command=lambda: download_report("Fares"), font=("Helvetica", 12)).pack(pady=5)
    tk.Button(download_tab, text="Download Routeing Guide", command=lambda: download_report("Routeing Guide"), font=("Helvetica", 12)).pack(pady=5)
    tk.Button(download_tab, text="Download Timetable", command=lambda: download_report("Timetable"), font=("Helvetica", 12)).pack(pady=5)

    # Settings Tab
    settings_tab = ttk.Frame(tab_control)
    tab_control.add(settings_tab, text="Settings")
    tk.Label(settings_tab, text="Update Settings", font=("Helvetica", 16)).pack(pady=10)

    # Current settings labels
    config = load_config()
    username = config["username"] if config["username"] else "Not set"
    password = config["password"]
    password_masked = '*' * len(password) if password else "Not set"
    save_location = config["save_location"] if config["save_location"] else "Not set"

    username_label = tk.Label(settings_tab, text=f"Username: {username}", font=("Helvetica", 12))
    username_label.pack(pady=5)
    password_label = tk.Label(settings_tab, text=f"Password: {password_masked}", font=("Helvetica", 12))
    password_label.pack(pady=5)
    location_label = tk.Label(settings_tab, text=f"Save Location: {save_location}", font=("Helvetica", 12))
    location_label.pack(pady=5)

    labels = {
        "username": username_label,
        "password": password_label,
        "location": location_label
    }

    # Update buttons
    tk.Button(settings_tab, text="Update Username", command=lambda: update_username_callback(labels), font=("Helvetica", 12)).pack(pady=5)
    tk.Button(settings_tab, text="Update Password", command=lambda: update_password_callback(labels), font=("Helvetica", 12)).pack(pady=5)
    tk.Button(settings_tab, text="Update Save Location", command=lambda: update_save_location_callback(labels), font=("Helvetica", 12)).pack(pady=5)

    tab_control.pack(expand=1, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()
