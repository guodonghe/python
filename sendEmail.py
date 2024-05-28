import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
'''
smtplib: 用于连接到 SMTP 服务器并发送电子邮件。
MIMEMultipart: 用于创建包含多个部分（例如正文和附件）的电子邮件。
MIMEText: 用于创建电子邮件正文。
MIMEBase: 用于创建附件。
encoders: 用于对附件进行编码。
os: 用于处理文件路径。
'''
def send_email(subject, body, to_address, from_address, from_password, attachment_path=None):
    # 创建一个邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    # 添加附件
    if attachment_path:
        attachment = MIMEBase('application', 'octet-stream')
        try:
            with open(attachment_path, 'rb') as attachment_file:
                attachment.set_payload(attachment_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(attachment)
        except Exception as e:
            print(f"Failed to attach file. Error: {e}")

    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP_SSL('smtp.ulucu.com', 465)
        server.ehlo()
        # 登录到服务器
        server.login(from_address, from_password)
        # 发送邮件
        server.sendmail(from_address, to_address, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        # 断开服务器连接
        server.quit()

if __name__ == "__main__":
    # 邮件信息
    from_address = 'monitor@ulu.com'
    from_password = 'Gbf'
    to_address = 'g@ulu.com'
    # to_address = '100399@qq.com'
    subject = 'Test Email'
    body = 'This is a test email sent from Python.'
    attachment_path = ''  # 例如 '/path/to/your/file.txt'

    # 发送邮件
    send_email(subject, body, to_address, from_address, from_password, attachment_path)
