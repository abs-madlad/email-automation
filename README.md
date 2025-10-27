# Mail to HR Automation

An automated email outreach tool designed to streamline job applications by sending personalized emails to HR professionals from an Excel spreadsheet.

## Features

- **Bulk Email Sending**: Send personalized emails to multiple HR contacts from an Excel file
- **Resume Attachment**: Automatically attach your resume to each email
- **Customizable Templates**: Use professional email templates with personalized fields
- **Batch Processing**: Send emails in configurable batch sizes to avoid rate limiting
- **Detailed Logging**: Track all email activities with comprehensive logs
- **Error Handling**: Robust validation and error handling for reliable operation

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mailToHr.git
   cd mailToHr
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the example:
   ```
   cp .env.example .env
   ```

4. Configure your `.env` file with your Gmail credentials and preferences.

## Configuration

Edit the `.env` file with your personal details:

```
GMAIL_APP_PASSWORD=your_gmail_app_password
GMAIL_EMAIL=your_email@gmail.com
RESUME_PATH=YourResume.pdf
EXCEL_FILE=HRexcel.xlsx
BATCH_SIZE=3
START_INDEX=0
```

**Important**: You need to use a Gmail App Password, not your regular Gmail password. [Learn how to create an App Password](https://support.google.com/accounts/answer/185833).

## Excel File Format

Your Excel file should contain the following columns:
- `HR Name`: The name of the HR contact
- `Company`: Company name
- `Email`: Email address of the HR contact

Example:
| HR Name | Company | Email |
|---------|---------|-------|
| John Doe | ABC Corp | john.doe@abccorp.com |
| Jane Smith | XYZ Inc | jane.smith@xyzinc.com |

## Usage

1. Update your personal details in the script (name, tech stack, LinkedIn profile)
2. Prepare your Excel file with HR contacts
3. Run the script:
   ```
   python script.py
   ```

The script will:
1. Load contacts from your Excel file
2. Send personalized emails with your resume attached
3. Log all activity to a timestamped log file
4. Display progress in the console

## Customization

You can customize the email templates and subject lines by editing the corresponding sections in `script.py`.

## License

MIT

## Author

Kanishk Vikram Singh
