#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from user_auth import UserAuth
from email.utils import formatdate, parsedate_to_datetime
import datetime
import json
import uuid
from email_db import EmailDatabase  # Import the EmailDatabase class

# Load environment variables
load_dotenv()

class LoginRegisterFrame(ttk.Frame):
    """Login and registration frame"""
    def __init__(self, master, auth_callback, parent_app):
        super().__init__(master, padding=20)
        self.master = master
        self.auth_callback = auth_callback
        self.parent_app = parent_app
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a6ea9"
        self.text_color = "#333333"
        self.error_color = "#e74c3c"
        self.success_color = "#2ecc71"
        
        # Create a notebook for login/register tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create login frame
        self.login_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.login_frame, text="Login")
        
        # Create register frame
        self.register_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.register_frame, text="Register")
        
        # Set up login form
        self.setup_login_form()
        
        # Set up register form
        self.setup_register_form()
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def setup_login_form(self):
        """Set up the login form"""
        # Create a header
        header_label = ttk.Label(
            self.login_frame, 
            text="Login to Your Account",
            font=("Arial", 14, "bold"),
            foreground=self.accent_color
        )
        header_label.pack(pady=(0, 20))
        
        # Email frame
        email_frame = ttk.Frame(self.login_frame)
        email_frame.pack(fill=tk.X, pady=(0, 10))
        
        email_label = ttk.Label(email_frame, text="Email:", width=10)
        email_label.pack(side=tk.LEFT)
        
        self.login_email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.login_email_var, width=30)
        email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password frame
        password_frame = ttk.Frame(self.login_frame)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        password_label = ttk.Label(password_frame, text="Password:", width=10)
        password_label.pack(side=tk.LEFT)
        
        self.login_password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.login_password_var, show="*", width=30)
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Login button
        login_button = ttk.Button(
            self.login_frame,
            text="Login",
            command=self.handle_login
        )
        login_button.pack(pady=10)
        
        # Status message
        self.login_status_var = tk.StringVar()
        self.login_status = ttk.Label(
            self.login_frame,
            textvariable=self.login_status_var,
            foreground=self.error_color
        )
        self.login_status.pack(pady=(10, 0))
    
    def setup_register_form(self):
        """Set up the registration form"""
        # Create a header
        header_label = ttk.Label(
            self.register_frame, 
            text="Create New Account",
            font=("Arial", 14, "bold"),
            foreground=self.accent_color
        )
        header_label.pack(pady=(0, 20))
        
        # Username frame
        username_frame = ttk.Frame(self.register_frame)
        username_frame.pack(fill=tk.X, pady=(0, 10))
        
        username_label = ttk.Label(username_frame, text="Username:", width=10)
        username_label.pack(side=tk.LEFT)
        
        self.reg_username_var = tk.StringVar()
        username_entry = ttk.Entry(username_frame, textvariable=self.reg_username_var, width=30)
        username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Email frame
        email_frame = ttk.Frame(self.register_frame)
        email_frame.pack(fill=tk.X, pady=(0, 10))
        
        email_label = ttk.Label(email_frame, text="Email:", width=10)
        email_label.pack(side=tk.LEFT)
        
        self.reg_email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.reg_email_var, width=30)
        email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password frame
        password_frame = ttk.Frame(self.register_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        password_label = ttk.Label(password_frame, text="Password:", width=10)
        password_label.pack(side=tk.LEFT)
        
        self.reg_password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.reg_password_var, show="*", width=30)
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Confirm Password frame
        confirm_frame = ttk.Frame(self.register_frame)
        confirm_frame.pack(fill=tk.X, pady=(0, 20))
        
        confirm_label = ttk.Label(confirm_frame, text="Confirm:", width=10)
        confirm_label.pack(side=tk.LEFT)
        
        self.reg_confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(confirm_frame, textvariable=self.reg_confirm_var, show="*", width=30)
        confirm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Register button
        register_button = ttk.Button(
            self.register_frame,
            text="Register",
            command=self.handle_register
        )
        register_button.pack(pady=10)
        
        # Status message
        self.register_status_var = tk.StringVar()
        self.register_status = ttk.Label(
            self.register_frame,
            textvariable=self.register_status_var,
            foreground=self.error_color
        )
        self.register_status.pack(pady=(10, 0))
    
    def handle_login(self):
        """Handle login form submission"""
        email = self.login_email_var.get()
        password = self.login_password_var.get()
        
        # Validate input
        if not email or not password:
            self.login_status_var.set("Email and password are required")
            self.login_status.config(foreground=self.error_color)
            return
        
        # Attempt to login
        auth = self.parent_app.auth
        result = auth.login(email, password)
        
        if result['success']:
            self.login_status_var.set("Login successful")
            self.login_status.config(foreground=self.success_color)
            # Call authentication callback with the user
            self.auth_callback(result['user'])
        else:
            self.login_status_var.set(result['error'])
            self.login_status.config(foreground=self.error_color)
    
    def handle_register(self):
        """Handle registration form submission"""
        username = self.reg_username_var.get()
        email = self.reg_email_var.get()
        password = self.reg_password_var.get()
        confirm = self.reg_confirm_var.get()
        
        # Validate input
        if not username or not email or not password:
            self.register_status_var.set("All fields are required")
            self.register_status.config(foreground=self.error_color)
            return
        
        if password != confirm:
            self.register_status_var.set("Passwords do not match")
            self.register_status.config(foreground=self.error_color)
            return
        
        # Validate email format
        if not self.is_valid_email(email):
            self.register_status_var.set("Invalid email format")
            self.register_status.config(foreground=self.error_color)
            return
        
        # Register the user
        auth = self.parent_app.auth
        result = auth.register_user(username, email, password)
        
        if result['success']:
            self.register_status_var.set("Registration successful! You can now login.")
            self.register_status.config(foreground=self.success_color)
            # Clear the form
            self.reg_username_var.set("")
            self.reg_email_var.set("")
            self.reg_password_var.set("")
            self.reg_confirm_var.set("")
            # Switch to login tab
            self.notebook.select(0)
        else:
            self.register_status_var.set(result['error'])
            self.register_status.config(foreground=self.error_color)
    
    def is_valid_email(self, email):
        """Check if email has valid format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class MailClientApp(tk.Tk):
    """Mail client application with authentication"""
    def __init__(self):
        super().__init__()
        self.title("SMTP Mail Client")
        self.geometry("800x600")
        self.minsize(700, 550)
        
        # Configure theme and colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a6ea9"
        self.text_color = "#333333"
        self.error_color = "#e74c3c"
        self.success_color = "#2ecc71"
        self.warning_color = "#f39c12"
        
        self.configure(bg=self.bg_color)
        
        # Initialize authentication
        self.auth = UserAuth()
        
        # Set default mailbox directory
        self.mailbox_dir = "mailboxes"
        
        # Set default SMTP settings from environment variables
        self.smtp_host = os.getenv("SMTP_HOST", "127.0.0.1")
        self.smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        
        # Create a frame for the content
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Check if user is already logged in
        self.current_user = None
        
        # Initialize status_var here to fix the error
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Initialize the email database
        self.email_db = EmailDatabase()
        
        # Show login/register view
        self.show_login_view()
    
    def show_login_view(self):
        """Show the login and registration view"""
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create login/register frame
        self.login_register_frame = LoginRegisterFrame(
            self.content_frame, 
            self.handle_authentication,
            self
        )
    
    def show_mail_client(self):
        """Show the mail client view"""
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create a main frame
        main_frame = ttk.Frame(self.content_frame, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header with user info and logout button
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="SMTP Mail Client", 
            font=("Arial", 18, "bold"),
            foreground=self.accent_color
        )
        title_label.pack(side=tk.LEFT)
        
        # User info
        user_info = ttk.Label(
            header_frame,
            text=f"Logged in as: {self.current_user['email']}",
            font=("Arial", 10),
            foreground=self.text_color
        )
        user_info.pack(side=tk.LEFT, padx=15)
        
        # Server info
        server_info = ttk.Label(
            header_frame,
            text=f"Server: {self.smtp_host}:{self.smtp_port}",
            font=("Arial", 10),
            foreground=self.text_color
        )
        server_info.pack(side=tk.LEFT, padx=5)
        
        # Logout button
        logout_button = ttk.Button(
            header_frame, 
            text="Logout",
            command=self.handle_logout
        )
        logout_button.pack(side=tk.RIGHT)
        
        # Create a tabbed interface
        tab_control = ttk.Notebook(main_frame)
        
        # Compose email tab
        compose_tab = ttk.Frame(tab_control, padding=10)
        tab_control.add(compose_tab, text="Compose Email")
        
        # View mailboxes tab
        mailbox_tab = ttk.Frame(tab_control, padding=10)
        tab_control.add(mailbox_tab, text="My Inbox")
        
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Set up the compose tab
        self.setup_compose_tab(compose_tab)
        
        # Set up the mailbox tab
        self.setup_mailbox_tab(mailbox_tab)
        
        # Status bar at the bottom - remove the redefinition of status_var here
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            foreground=self.text_color,
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
    
    def setup_compose_tab(self, parent):
        """Set up the compose email tab"""
        # Auto-fill sender from current user
        sender_email = self.current_user['email']
        
        # Recipient frame
        recipient_frame = ttk.Frame(parent)
        recipient_frame.pack(fill=tk.X, pady=(0, 5))
        
        recipient_label = ttk.Label(recipient_frame, text="To:", width=10)
        recipient_label.pack(side=tk.LEFT)
        
        self.recipient_var = tk.StringVar()
        self.recipient_var.trace("w", self.check_recipient)
        
        self.recipient_entry = ttk.Entry(recipient_frame, textvariable=self.recipient_var)
        self.recipient_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.recipient_status = ttk.Label(recipient_frame, text="", width=20)
        self.recipient_status.pack(side=tk.LEFT, padx=5)
        
        # Subject frame
        subject_frame = ttk.Frame(parent)
        subject_frame.pack(fill=tk.X, pady=(0, 5))
        
        subject_label = ttk.Label(subject_frame, text="Subject:", width=10)
        subject_label.pack(side=tk.LEFT)
        
        self.subject_var = tk.StringVar()
        subject_entry = ttk.Entry(subject_frame, textvariable=self.subject_var)
        subject_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 25))
        
        # Message body
        body_frame = ttk.Frame(parent)
        body_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        body_label = ttk.Label(body_frame, text="Message:", width=10, anchor=tk.NW)
        body_label.pack(side=tk.LEFT, anchor=tk.N)
        
        self.body_text = scrolledtext.ScrolledText(
            body_frame, 
            wrap=tk.WORD,
            height=10
        )
        self.body_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X)
        
        self.send_button = ttk.Button(
            buttons_frame, 
            text="Send Email",
            command=self.send_email
        )
        self.send_button.pack(side=tk.RIGHT)
        
        clear_button = ttk.Button(
            buttons_frame, 
            text="Clear",
            command=self.clear_compose_form
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
    
    def setup_mailbox_tab(self, parent):
        """Set up the mailbox tab for viewing user's inbox"""
        mailbox_frame = ttk.Frame(parent)
        mailbox_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top frame for refresh button and search
        top_frame = ttk.Frame(mailbox_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Refresh button
        refresh_button = ttk.Button(
            top_frame,
            text="Refresh",
            command=self.view_user_inbox
        )
        refresh_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add search functionality
        search_label = ttk.Label(top_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        search_button = ttk.Button(
            top_frame,
            text="Search",
            command=self.search_emails
        )
        search_button.pack(side=tk.LEFT)
        
        clear_search_button = ttk.Button(
            top_frame,
            text="Clear",
            command=self.clear_search
        )
        clear_search_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Create a scrollable treeview for emails
        treeview_frame = ttk.Frame(mailbox_frame)
        treeview_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Email list with scrollbars
        tree_scroll_y = ttk.Scrollbar(treeview_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.email_tree = ttk.Treeview(
            treeview_frame,
            columns=("id", "from", "subject", "date"),
            show="headings",
            height=10
        )
        
        # Configure columns
        self.email_tree.heading("id", text="#")
        self.email_tree.heading("from", text="From")
        self.email_tree.heading("subject", text="Subject")
        self.email_tree.heading("date", text="Date")
        
        self.email_tree.column("id", width=50, stretch=False)
        self.email_tree.column("from", width=200)
        self.email_tree.column("subject", width=300)
        self.email_tree.column("date", width=150)
        
        # Connect scrollbars
        self.email_tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        tree_scroll_y.configure(command=self.email_tree.yview)
        tree_scroll_x.configure(command=self.email_tree.xview)
        
        self.email_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event to view email
        self.email_tree.bind("<Double-1>", self.view_selected_email)
        
        # Add delete button below the treeview
        delete_button = ttk.Button(
            mailbox_frame,
            text="Delete Selected Email",
            command=self.delete_selected_email
        )
        delete_button.pack(anchor=tk.E, pady=(0, 10))
        
        # Email view frame
        email_view_frame = ttk.LabelFrame(mailbox_frame, text="Email Content")
        email_view_frame.pack(fill=tk.BOTH, expand=True)
        
        self.email_content = scrolledtext.ScrolledText(
            email_view_frame, 
            wrap=tk.WORD,
            height=10,
            state="disabled"
        )
        self.email_content.pack(fill=tk.BOTH, expand=True)
        
        # Automatically load user's inbox
        self.view_user_inbox()
    
    def view_user_inbox(self):
        """View emails in the user's inbox"""
        if not self.current_user:
            return
            
        self.status_var.set(f"Loading emails for {self.current_user['email']}...")
        
        # Clear the treeview
        for item in self.email_tree.get_children():
            self.email_tree.delete(item)
        
        # Clear the email content
        self.email_content.config(state="normal")
        self.email_content.delete(1.0, tk.END)
        self.email_content.config(state="disabled")
        
        # Get user's email
        email = self.current_user['email']
        
        # Try to use database first, fall back to file system if needed
        use_db = os.path.exists("database/emails.db")
        
        if use_db:
            # Get emails from database
            emails = self.email_db.get_mailbox(email)
            
            if not emails:
                self.status_var.set(f"No emails found in mailbox for {email}")
                return
            
            # Add emails to the treeview
            for i, mail in enumerate(emails, 1):
                sender = mail['sender']
                subject = mail['subject']
                date_str = mail['received_date']
                
                try:
                    # Try to format the date nicely
                    date_obj = datetime.fromisoformat(date_str)
                    date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    # If parsing fails, use the original date string
                    pass
                
                # Insert with database ID as tag
                self.email_tree.insert("", "end", values=(i, sender, subject, date_str), 
                                      tags=(mail['id'], 'db'))
            
            self.status_var.set(f"Loaded {len(emails)} emails for {self.current_user['email']}")
            
        else:
            # Fall back to file system
            user_dir = email.replace('@', '_at_').replace('.', '_dot_')
            mailbox_path = os.path.join(self.mailbox_dir, user_dir)
            
            if not os.path.exists(mailbox_path):
                self.status_var.set(f"No mailbox found for {email}")
                return
            
            # Get all .eml files
            import glob
            import email
            from email.policy import default
            
            email_files = sorted(glob.glob(os.path.join(mailbox_path, "*.eml")))
            
            if not email_files:
                self.status_var.set(f"No emails found in mailbox for {email}")
                return
            
            # Add emails to the treeview
            for i, email_file in enumerate(email_files, 1):
                with open(email_file, 'rb') as f:
                    msg = email.message_from_binary_file(f, policy=default)
                    sender = msg.get("From", "Unknown")
                    subject = msg.get("Subject", "No Subject")
                    
                    # Get date and format it nicely
                    date_str = msg.get("Date", "Unknown Date")
                    try:
                        if date_str != 'Unknown Date':
                            # Try to parse and format the date
                            date_obj = parsedate_to_datetime(date_str)
                            date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        # If parsing fails, use the original date string
                        pass
                    
                    # Tag with file path and 'file' tag
                    self.email_tree.insert("", "end", values=(i, sender, subject, date_str), 
                                          tags=(email_file, 'file'))
            
            self.status_var.set(f"Loaded {len(email_files)} emails for {self.current_user['email']}")
    
    def view_selected_email(self, event):
        """View the selected email"""
        selection = self.email_tree.selection()
        
        if not selection:
            return
        
        # Get the item and its tags
        item = selection[0]
        tags = self.email_tree.item(item, "tags")
        email_id = tags[0]
        source_type = tags[1] if len(tags) > 1 else 'file'  # Default to file if not specified
        
        if source_type == 'db':
            # Read from database
            mail_data = self.email_db.get_email(email_id)
            
            if not mail_data:
                self.status_var.set(f"Error: Email not found in database")
                return
                
            # Mark as read
            self.email_db.mark_as_read(email_id)
            
            # Clear content and add email details
            self.email_content.config(state="normal")
            self.email_content.delete(1.0, tk.END)
            
            # Format date if possible
            date_str = mail_data['received_date']
            try:
                date_obj = datetime.fromisoformat(date_str)
                date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
                
            # Add headers
            self.email_content.insert(tk.END, f"From: {mail_data['sender']}\n")
            self.email_content.insert(tk.END, f"To: {mail_data['recipient']}\n")
            self.email_content.insert(tk.END, f"Subject: {mail_data['subject']}\n")
            self.email_content.insert(tk.END, f"Date: {date_str}\n")
            
            # Add attachments if any
            if mail_data['attachments']:
                try:
                    attachments = json.loads(mail_data['attachments'])
                    if attachments:
                        self.email_content.insert(tk.END, "Attachments: ")
                        self.email_content.insert(tk.END, ", ".join(attachments) + "\n")
                except:
                    pass
                    
            self.email_content.insert(tk.END, "-" * 60 + "\n")
            
            # Add body
            self.email_content.insert(tk.END, mail_data['body'])
            
        else:
            # Read from file (existing implementation)
            email_file = email_id
            import email
            from email.policy import default
            
            with open(email_file, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=default)
                
                # Clear the content area
                self.email_content.config(state="normal")
                self.email_content.delete(1.0, tk.END)
                
                # Get date and format it nicely if possible
                date_str = msg.get('Date', 'Unknown Date')
                try:
                    if date_str != 'Unknown Date':
                        # Try to parse and format the date nicely
                        date_obj = parsedate_to_datetime(date_str)
                        date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    # If parsing fails, use the original date string
                    pass
                
                # Add email headers
                self.email_content.insert(tk.END, f"From: {msg.get('From', 'Unknown')}\n")
                self.email_content.insert(tk.END, f"To: {msg.get('To', 'Unknown')}\n")
                self.email_content.insert(tk.END, f"Subject: {msg.get('Subject', 'No Subject')}\n")
                self.email_content.insert(tk.END, f"Date: {date_str}\n")
                self.email_content.insert(tk.END, "-" * 60 + "\n")
                
                # Add email body
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    # Skip attachments
                    if "attachment" in content_disposition:
                        self.email_content.insert(tk.END, f"[Attachment: {part.get_filename()}]\n")
                        continue
                    
                    if content_type == "text/plain":
                        self.email_content.insert(tk.END, part.get_content())
        
        self.email_content.config(state="disabled")
    
    def check_recipient(self, *args):
        """Check if recipient email is valid and has a mailbox"""
        email = self.recipient_var.get()
        
        if not email:
            self.recipient_status.config(text="")
            return
        
        if not self.is_valid_email(email):
            self.recipient_status.config(text="Invalid format", foreground=self.error_color)
            return
        
        if self.email_exists_locally(email):
            self.recipient_status.config(text="Local mailbox exists", foreground=self.success_color)
        else:
            self.recipient_status.config(text="No local mailbox", foreground=self.warning_color)
    
    def is_valid_email(self, email):
        """Check if email has valid format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def email_exists_locally(self, email):
        """Check if an email address has a mailbox in the system"""
        if not self.is_valid_email(email):
            return False
        
        # Check in database if available
        if os.path.exists("database/emails.db"):
            # Just verify email format, can't check if recipient exists in DB beforehand
            return True
            
        # Fallback to file system check
        user = email.replace('@', '_at_').replace('.', '_dot_')
        mailbox_path = os.path.join(self.mailbox_dir, user)
        return os.path.exists(mailbox_path)
    
    def clear_compose_form(self):
        """Clear the compose form"""
        self.recipient_var.set("")
        self.subject_var.set("")
        self.body_text.delete(1.0, tk.END)
    
    def send_email(self):
        """Send an email via SMTP with address verification"""
        try:
            # Get form values
            sender = self.current_user['email']
            recipient = self.recipient_var.get()
            subject = self.subject_var.get()
            body = self.body_text.get(1.0, tk.END).strip()
            
            # Validate form
            if not recipient:
                messagebox.showerror("Error", "Recipient email is required")
                return
            
            if not subject:
                subject = "(No Subject)"
            
            # Verify recipient email format
            if not self.is_valid_email(recipient):
                messagebox.showerror("Error", f"Invalid recipient email format: {recipient}")
                return
            
            # Check if recipient has a local mailbox
            if not self.email_exists_locally(recipient):
                if not messagebox.askyesno("Warning", 
                    f"{recipient} doesn't have a local mailbox. Messages might not be delivered.\n\nDo you want to continue?"):
                    return
            
            # Create the email
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = recipient
            message["Subject"] = subject
            
            # Add current date and time in RFC 2822 format
            message["Date"] = formatdate(localtime=True)
            
            # Add body to email
            message.attach(MIMEText(body, "plain"))
            
            self.status_var.set(f"Connecting to SMTP server at {self.smtp_host}:{self.smtp_port}...")
            self.update_idletasks()
            
            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                # Send the email
                server.sendmail(sender, recipient, message.as_string())
                
                # Check if recipient has a local mailbox
                if self.email_exists_locally(recipient):
                    self.status_var.set(f"Email sent successfully to {recipient} (local mailbox exists)")
                else:
                    self.status_var.set(f"Email sent successfully to {recipient} (no local mailbox - message might be lost)")
                
                messagebox.showinfo("Success", "Email sent successfully!")
                
                # Clear the form after successful send
                self.clear_compose_form()
        except Exception as e:
            self.status_var.set(f"Error sending email: {e}")
            messagebox.showerror("Error", f"Error sending email: {e}")
    
    def handle_authentication(self, user):
        """Handle successful authentication"""
        self.current_user = user
        self.show_mail_client()
    
    def handle_logout(self):
        """Handle user logout"""
        self.auth.logout()
        self.current_user = None
        self.show_login_view()
        
    def search_emails(self):
        """Search emails in the user's mailbox"""
        if not self.current_user:
            return
        
        # Get search query
        query = self.search_var.get().strip()
        if not query:
            self.status_var.set("Please enter a search term")
            return
        
        email_address = self.current_user['email']
        self.status_var.set(f"Searching for '{query}' in {email_address}'s mailbox...")
        
        # Only database supports search
        if not os.path.exists("database/emails.db"):
            messagebox.showinfo("Search unavailable", 
                "Search functionality requires database storage. Please run the migrate_to_db.py script first.")
            return
        
        # Clear the treeview
        for item in self.email_tree.get_children():
            self.email_tree.delete(item)
        
        # Search emails in database
        emails = self.email_db.search_emails(email_address, query)
        
        if not emails:
            self.status_var.set(f"No emails found matching '{query}'")
            return
        
        # Add search results to the treeview
        for i, mail in enumerate(emails, 1):
            sender = mail['sender']
            subject = mail['subject']
            date_str = mail['received_date']
            
            try:
                # Try to format the date nicely
                date_obj = datetime.fromisoformat(date_str)
                date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except:
                # If parsing fails, use the original date string
                pass
            
            # Insert with database ID as tag
            self.email_tree.insert("", "end", values=(i, sender, subject, date_str), 
                                  tags=(mail['id'], 'db'))
        
        self.status_var.set(f"Found {len(emails)} emails matching '{query}'")

    def clear_search(self):
        """Clear search and reload inbox"""
        self.search_var.set("")
        self.view_user_inbox()

    def delete_selected_email(self):
        """Delete the selected email"""
        selection = self.email_tree.selection()
        
        if not selection:
            messagebox.showinfo("No Selection", "Please select an email to delete")
            return
        
        # Get the item and its tags
        item = selection[0]
        tags = self.email_tree.item(item, "tags")
        email_id = tags[0]
        source_type = tags[1] if len(tags) > 1 else 'file'  # Default to file if not specified
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this email?"):
            return
        
        try:
            if source_type == 'db':
                # Delete from database
                if self.email_db.delete_email(email_id):
                    self.status_var.set("Email deleted successfully from database")
                else:
                    messagebox.showerror("Error", "Failed to delete email from database")
                    return
            else:
                # Delete from file system
                email_file = email_id
                os.remove(email_file)
                self.status_var.set("Email deleted successfully from file system")
            
            # Remove from UI
            self.email_tree.delete(item)
            
            # Clear the content area
            self.email_content.config(state="normal")
            self.email_content.delete(1.0, tk.END)
            self.email_content.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete email: {e}")
            self.status_var.set(f"Error deleting email: {e}")

def main():
    app = MailClientApp()
    app.mainloop()

if __name__ == "__main__":
    main() 