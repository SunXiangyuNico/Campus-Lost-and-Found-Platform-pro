import os
# import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from twilio.rest import Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def send_email(to_email, subject, html_content):
    """
    通用邮件发送函数
    """
    # 从环境变量中获取邮件配置
    sender_email = os.environ.get('MAIL_USERNAME')
    sender_password = os.environ.get('MAIL_PASSWORD')
    smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', 587))

    if not all([sender_email, sender_password]):
        print("Mail server not configured. Skipping email.")
        return

    # 创建邮件对象
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    # 附加HTML内容
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        # 连接到SMTP服务器并发送邮件的功能已被禁用，以解决SSL冲突
        print(f"Email sending is disabled. Would have sent to {to_email}.")
        # with smtplib.SMTP(smtp_server, smtp_port) as server:
        #     server.starttls()  # 启用安全传输
        #     server.login(sender_email, sender_password)
        #     server.sendmail(sender_email, to_email, msg.as_string())
        #     print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"An error occurred in the disabled email function: {e}")

def send_sms(to_phone_number, body):
    """
    使用 Twilio 发送短信。
    
    :param to_phone_number: 收件人的手机号码 (格式: '+861234567890')。
    :param body: 短信内容。
    :return: 成功时返回 True，失败时返回 False。
    """
    # 从环境变量中获取 Twilio 的凭证和电话号码
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

    if not all([account_sid, auth_token, twilio_phone_number]):
        print("Error: Twilio credentials not configured in .env file.")
        return False

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        print(f"SMS sent to {to_phone_number}, SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

# --- 测试用例 ---
# 您可以在开发时取消下面的注释来直接测试这两个函数
# if __name__ == '__main__':
#     from dotenv import load_dotenv
#     load_dotenv(dotenv_path='../.env') # 加载 .env 文件
#
#     # 测试邮件发送
#     email_success = send_email(
#         to_email='YOUR_TEST_EMAIL@example.com', # <--- 请替换为你的测试接收邮箱
#         subject='来自校园失物招领平台的测试邮件（QQ邮箱）',
#         html_content='<strong>这是一封通过QQ邮箱SMTP发送的测试邮件，恭喜您，邮件服务已成功配置！</strong>'
#     )
#     print(f"Email test successful: {email_success}")
#
#     # 测试短信发送 (如果需要测试，请确保Twilio凭证已配置)
#     # sms_success = send_sms(
#     #     to_phone_number='+861234567890', # <--- 请替换为你的测试手机号
#     #     body='【校园失物招领】您的验证码是：123456。该验证码5分钟内有效。'
#     # )
#     # print(f"SMS test successful: {sms_success}") 