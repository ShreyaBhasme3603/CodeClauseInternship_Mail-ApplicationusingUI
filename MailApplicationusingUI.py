import tkinter as tk
from tkinter import messagebox
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail Application")
        self.root.geometry("400x300")

        # Create database connection
        self.conn = sqlite3.connect("mail_app.db")
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                smtp_server TEXT,
                smtp_port INTEGER,
                email_address TEXT
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sent_emails (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                recipient TEXT,
                subject TEXT,
                body TEXT,
                sent_at TEXT
            );
        """)
        self.conn.commit()

        # Create UI components
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack()

        self.smtp_server_label = tk.Label(root, text="SMTP Server:")
        self.smtp_server_label.pack()
        self.smtp_server_entry = tk.Entry(root, width=30)
        self.smtp_server_entry.pack()

        self.smtp_port_label = tk.Label(root, text="SMTP Port:")
        self.smtp_port_label.pack()
        self.smtp_port_entry = tk.Entry(root, width=30)
        self.smtp_port_entry.pack()

        self.email_address_label = tk.Label(root, text="Email Address:")
        self.email_address_label.pack()
        self.email_address_entry = tk.Entry(root, width=30)
        self.email_address_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.compose_button = tk.Button(root, text="Compose", command=self.compose_email)
        self.compose_button.pack()

        # self.sent_emails_button = tk.Button(root, text="Sent Emails", command=self.view_sent_emails)
        # self.sent_emails_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        smtp_server = self.smtp_server_entry.get()
        smtp_port = int(self.smtp_port_entry.get())
        email_address = self.email_address_entry.get()

        # Check if user exists in database
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user:
            # Check if password is correct
            if user[1] == password:
                # Store user configuration in database
                self.cursor.execute("UPDATE users SET smtp_server=?, smtp_port=?, email_address=? WHERE username=?", (smtp_server, smtp_port, email_address, username))
                self.conn.commit()
                messagebox.showinfo("Login", "Login successful!")
            else:
                messagebox.showerror("Login", "Invalid password")
        else:
            # Create new user in database
            self.cursor.execute("INSERT INTO users (username, password, smtp_server, smtp_port, email_address) VALUES (?, ?, ?, ?, ?)", (username, password, smtp_server, smtp_port, email_address))
            self.conn.commit()
            messagebox.showinfo("Login", "User created successfully!")

    def compose_email(self):
        # Create email composition window
        compose_window = tk.Toplevel(self.root)
        compose_window.title("Compose Email")

        recipient_label = tk.Label(compose_window, text="Recipient:")
        recipient_label.pack()
        recipient_entry = tk.Entry(compose_window, width=30)
        recipient_entry.pack()

        subject_label = tk.Label(compose_window, text="Subject:")
        subject_label.pack()
        subject_entry = tk.Entry(compose_window, width=30)
        subject_entry.pack()

        body_label = tk.Label(compose_window, text="Body:")
        body_label.pack()
        body_text = tk.Text(compose_window, width=30, height=10)
        body_text.pack()

        send_button = tk.Button(compose_window, text="Send", command=lambda: self.send_email(recipient_entry.get(), subject_entry.get(), body_text.get("1.0", "end-1c")))
        send_button.pack()

    def send_email(self, recipient, subject, body):
        # Get user configuration from database
        self.cursor.execute("SELECT * FROM users WHERE username=?", (self.username_entry.get(),))
        user = self.cursor
    
if __name__ == "__main__":
    root = tk.Tk()
    music_player = MailApp(root)
    root.mainloop()