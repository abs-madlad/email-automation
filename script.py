import pandas as pd
import yagmail
import time
import random
import re
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Directly read from .env file as a fallback
if os.path.exists('.env'):
    with open('.env', 'r') as env_file:
        for line in env_file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# --- YOUR DETAILS ---
your_name = "Kanishk Vikram Singh"
your_tech_stack = "Next.js, React.js, Node.js, Express.js, MongoDB, Python"
your_linkedin = "https://www.linkedin.com/in/kanishk-vikram-singh"

# Load from environment variables
your_email = os.environ.get("GMAIL_EMAIL", "kanishkonwork@gmail.com")
your_app_password = os.environ.get("GMAIL_APP_PASSWORD")
resume_path = os.environ.get("RESUME_PATH", "KanishkFullStack.pdf")
excel_file = os.environ.get("EXCEL_FILE", "Sample.xlsx")
batch_size = int(os.environ.get("BATCH_SIZE", "97"))
start_index = int(os.environ.get("START_INDEX", "3"))

# --- VALIDATION FUNCTIONS ---
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_configuration():
    """Validate configuration before running"""
    if not your_app_password:
        print("❌ Please set your Gmail app password in the .env file!")
        print("   Set GMAIL_APP_PASSWORD=your_actual_app_password")
        return False
    
    if not os.path.exists(excel_file):
        print(f"❌ {excel_file} file not found!")
        return False
    
    if resume_path and not os.path.exists(resume_path):
        print(f"⚠️ Resume file '{resume_path}' not found. Emails will be sent without attachment.")
    
    return True

# --- LOGGING SETUP ---
logging.basicConfig(
    filename=f'email_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- VALIDATE CONFIGURATION ---
if not validate_configuration():
    exit(1)

# --- LOAD DATA ---
try:
    df = pd.read_excel(excel_file)
    print(f"📊 Loaded {len(df)} records from {excel_file}")
except Exception as e:
    print(f"❌ Error loading Excel file: {str(e)}")
    exit(1)

# --- INITIALIZE EMAIL CLIENT ---
try:
    yag = yagmail.SMTP(your_email, your_app_password)
    print("✅ Email client initialized successfully")
except Exception as e:
    print(f"❌ Error initializing email client: {str(e)}")
    exit(1)

# --- TRACKING SETUP ---
sent_emails = set()  # Track sent emails to avoid duplicates

subject_lines = [
    "Inquiry Regarding Full Stack Developer Opportunities",
    "Exploring Full Stack Developer Roles at Your Team",
    "Full Stack Developer | Checking for Openings"
]

def professional_template(hr_name, company):
    return f"""Hi {hr_name},

I hope you're doing well.

My name is {your_name}, and I am a Full Stack Developer experienced in:
{your_tech_stack}.

I came across {company} and was impressed by the work being done there.
I wanted to inquire if there are any Full Stack Developer openings currently available.

I would be glad to share my resume (attached) or have a brief discussion if possible.

Best regards,
{your_name}
LinkedIn: {your_linkedin}
"""

def friendly_template(hr_name, company):
    return f"""Hey {hr_name}, hope you're doing great 😊

Hope you're having a great day 😊

I'm {your_name}, a Full Stack Developer working with:
{your_tech_stack}.

I've been following {company} for a bit and really liked what your team is building.
Just wanted to check if you're hiring Full Stack Developers right now — would love to explore!

I've attached my resume for your review.

Thanks!
{your_name}
LinkedIn: {your_linkedin}
"""

def bold_template(hr_name, company):
    return f"""Hi {hr_name},

I'm {your_name} and the following is my tech stack: ({your_tech_stack}). I'm interested in joining {company}.
Are there openings for Full Stack Developers currently?

Please find my resume attached for your consideration.

Thanks,
{your_name}
LinkedIn: {your_linkedin}
"""

# --- BATCH CONTROL ---
# Batch settings are now loaded from environment variables

end_index = min(start_index + batch_size, len(df))

print(f"📌 Sending emails from index {start_index} to {end_index - 1}")
print(f"📎 Resume attachment: {'Yes' if resume_path and os.path.exists(resume_path) else 'No'}")

# --- STATISTICS TRACKING ---
successful_sends = 0
failed_sends = 0
skipped_duplicates = 0
skipped_invalid = 0

for i in range(start_index, end_index):
    row = df.iloc[i]
    hr_name = row["Name"]
    hr_email = row["Email"]
    company = row["Company"]

    # Skip if email already sent
    if hr_email in sent_emails:
        print(f"⏭️ Skipping {hr_name} - already sent")
        skipped_duplicates += 1
        continue

    # Validate email format
    if not is_valid_email(hr_email):
        print(f"❌ Invalid email format for {hr_name}: {hr_email}")
        skipped_invalid += 1
        logging.warning(f"Invalid email format: {hr_email}")
        continue

    # Tone rotation every 10
    if (i // 10) % 3 == 0:
        body = professional_template(hr_name, company)
        tone_used = "Professional"
    elif (i // 10) % 3 == 1:
        body = friendly_template(hr_name, company)
        tone_used = "Friendly"
    else:
        body = bold_template(hr_name, company)
        tone_used = "Bold"

    subject = random.choice(subject_lines)

    # Prepare attachments
    attachments = []
    if resume_path and os.path.exists(resume_path):
        attachments = [resume_path]

    # Send email with error handling
    try:
        yag.send(to=hr_email, subject=subject, contents=body, attachments=attachments)
        
        # Mark as sent and log success
        sent_emails.add(hr_email)
        successful_sends += 1
        
        print(f"✅ Sent ({tone_used}, Subject: '{subject}') to {hr_name} ({hr_email})")
        logging.info(f"SUCCESS: {hr_name} ({hr_email}) - {tone_used} tone")
        
    except Exception as e:
        failed_sends += 1
        error_msg = str(e)
        print(f"❌ Failed to send to {hr_name} ({hr_email}): {error_msg}")
        logging.error(f"FAILED: {hr_name} ({hr_email}) - {error_msg}")
        continue

    # Random delay between emails
    delay = random.randint(2, 6)
    time.sleep(delay)

# --- FINAL STATISTICS ---
print(f"\n📊 BATCH COMPLETED!")
print(f"✅ Successful sends: {successful_sends}")
print(f"❌ Failed sends: {failed_sends}")
print(f"⏭️ Skipped duplicates: {skipped_duplicates}")
print(f"🚫 Skipped invalid emails: {skipped_invalid}")
print(f"📧 Total processed: {successful_sends + failed_sends + skipped_duplicates + skipped_invalid}")

# Log final statistics
logging.info(f"BATCH COMPLETED - Success: {successful_sends}, Failed: {failed_sends}, Skipped: {skipped_duplicates + skipped_invalid}")

print("\n✨ Batch completed successfully!")
