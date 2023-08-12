import smtplib
from email.message import EmailMessage
import time

_Host = ''
_Port = ''
_From = ''
_To = ''
_Cc = ''
LOGFILE = ''
FILENAME = ''
MSG = ''

def __EmailAlert(MSG, num_retries = 2, retry_delay = 30):
    '''
    This will send alert mails for failed file with Importance as High.
    '''
    retry_count = 0
    while retry_count < num_retries:

        try:
            print("Sending email notification.")

            msg = EmailMessage()
            msg['Importance'] = 'High'
            msg['From'] = _From
            msg['To'] = _To
            msg['Cc'] = _Cc
            msg['Subject'] = f" "
            msg.set_content( f"""{MSG}""")
            with open(LOGFILE, 'rb') as f:
                __data = f.read()
                msg.add_attachment(__data, maintype='text', subtype='plain', filename=FILENAME)

            with smtplib.SMTP(_Host,_Port) as server:
                server.send_message(msg)
                server.quit()

            print("Mail sent successfully.")

            break

        except Exception as err:
            retry_count += 1

            if retry_count < num_retries:
                print(f"Unable to send email. {str(err)}\nRetrying in {retry_delay} sec.")
                time.sleep(retry_delay)
            else:
                print(f"Unable to send email. {str(err)}")

__EmailAlert(MSG=MSG)