# SMTP Email Server

A simple SMTP email server implementation that handles the email sending and receiving process as depicted in the standard email flow diagram.

## Features

- SMTP server that accepts and processes email messages
- Message Transfer Agent (MTA) functionality
- Local mailbox storage for received emails
- User authentication system with registration and login
- Personal mailbox access for registered users
- Email sending and reading with a modern graphical interface
- **SQLite database storage for emails** with backward compatibility for file-based storage
- **Email deletion functionality** for managing inbox contents

## Components

1. **SMTP Server**: Handles incoming email connections and processes messages
2. **Mailbox Manager**: Stores emails in user-specific mailboxes
3. **User Authentication System**: User registration, login, and mailbox management
4. **Mail Client**: Integrated client for sending and reading emails with user authentication
5. **Mail Reader**: Command-line utility for reading emails

## Setup

1. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

2. Configure the server by editing the `.env` file:
   ```
   SMTP_HOST=127.0.0.1  # Host to bind the SMTP server
   SMTP_PORT=1025       # Port to bind the SMTP server (use >1024 for non-root)
   ```

3. (Optional) Create test user accounts:
   ```bash
   python3 src/create_test_users.py
   ```
   This will create two test accounts:
   - Alice (email: alice@example.com, password: password123)
   - Bob (email: bob@example.com, password: password456)

## Usage

### Starting the SMTP Server

```bash
python3 src/smtp_server.py
```

The server will start and listen for SMTP connections on the configured host and port.

### Using the Mail Client

The user authentication mail client provides a graphical interface with user management:

```bash
python3 src/user_mail_client.py
```

Features:
- User registration system with secure password storage
- User login and session management
- Personal mailbox access for registered users
- Sending emails from authenticated accounts
- Reading emails from user's own mailbox
- Real-time validation of email addresses
- Warning when sending to non-existent mailboxes

**Login with test accounts:**
- Alice: Email: `alice@example.com`, Password: `password123`
- Bob: Email: `bob@example.com`, Password: `password456`

Or register your own account using the registration tab.

**Deleting Emails:**
1. Select an email in your inbox by clicking on it
2. Click the "Delete Selected Email" button
3. Confirm the deletion when prompted
4. The email will be permanently removed from both the database and the interface

### Reading Emails (Command-line)

List all mailboxes:
```bash
python3 src/mail_reader.py --list
```

List emails in a specific mailbox:
```bash
python3 src/mail_reader.py --mailbox user@example.com
```

Read a specific email:
```bash
python3 src/mail_reader.py --mailbox user@example.com --read 1
```

Use database storage instead of file system:
```bash
python3 src/mail_reader.py --mailbox user@example.com --use-db
```

Read a specific email by ID (database only):
```bash
python3 src/mail_reader.py --mailbox user@example.com --id email_id_here --use-db
```

### Testing the System

Send a test email between users:
```bash
python3 src/send_test_email.py
```
This will send a test email from Alice to Bob.

## Project Structure

The project contains the following files:

### Core Files
- `src/smtp_server.py` - The SMTP server implementation
- `src/user_auth.py` - User authentication system
- `src/user_mail_client.py` - Mail client with user authentication
- `src/mail_reader.py` - Command-line email reading utility

### Utility Files
- `src/create_test_mailboxes.py` - Helper to create test mailboxes
- `src/create_test_users.py` - Helper to create test user accounts
- `src/send_test_email.py` - Helper to send test emails between users

### Directory Structure
```
.
├── README.md
├── requirements.txt
├── .env
├── src/                        # Source code directory
├── logs/                       # Server logs
├── users/                      # User accounts data
├── mailboxes/                  # Stored emails (legacy format)
├── database/                   # Email database storage
└── config/                     # Configuration files
```

## Workflow

For daily use, follow these steps:

1. Start the SMTP server:
   ```bash
   python3 src/smtp_server.py
   ```

2. Run the mail client:
   ```bash
   python3 src/user_mail_client.py
   ```

3. Login with your credentials or register a new account

4. Send and receive emails through the graphical interface

## Implementation Details

### Security

- Passwords are securely hashed using SHA-256 with unique salts for each user
- User authentication is managed through a dedicated UserAuth class
- Email addresses are validated using regex pattern matching

### Data Storage

- User accounts are stored in JSON format in the users directory
- Emails are stored in a SQLite database in the database directory
- For backward compatibility, emails are also stored as .eml files in user-specific mailbox directories
- Mailbox names are derived from email addresses with special characters replaced

### User Interface

- Tkinter is used for the graphical user interface
- Tabbed interface for easy navigation between composing and reading emails
- Real-time validation of email addresses with visual feedback
- Status bar for operation feedback
- Email deletion with confirmation dialog to prevent accidental deletions

### Database Storage

- Emails are stored in a SQLite database for improved searchability and performance
- Database functionality is implemented in the `email_db.py` module
- The system provides backward compatibility with the file-based storage system
- Email read status tracking is available in database mode
- Search functionality allows finding emails by content or subject
- Emails can be permanently deleted from both the database and file system

## Troubleshooting

If you encounter issues with the user mail client:

1. Make sure the SMTP server is running (`python3 src/smtp_server.py`)
2. Check that user mailboxes exist (`ls -la mailboxes/`)
3. Verify user accounts in the users.json file (`cat users/users.json`)
4. Try restarting the mail client application

### Common Error Fixes

If you see errors related to the `status_var` attribute, make sure it's properly initialized in the MailClientApp class constructor.

## How It Works

1. **User Authentication**: Users register and login to access their personal mailbox
2. **Email Submission**: The mail client sends an email to the SMTP server
3. **Message Transfer**: The SMTP server processes the incoming email
4. **Message Delivery**: The email is stored in the recipient's mailbox
5. **Email Access**: Users can view their emails through the mail client interface
6. **Email Management**: Users can search, read, and delete emails from their mailbox

## Future Improvements

Potential improvements for this system include:
- Support for email attachments
- Email threading and conversation views
- Advanced email filtering and sorting
- Rich text (HTML) email composition
- Contact management system
- Improved security with SSL/TLS support
- Full migration to database storage with file storage removal
- Database backup and restore functionality
- Bulk email deletion for multiple selected emails
- Email archiving functionality as an alternative to deletion
- Trash folder with delayed permanent deletion

## License

MIT 