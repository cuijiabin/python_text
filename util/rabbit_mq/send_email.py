import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.exmail.qq.com"  # SMTP服务器
mail_user = "system_remind@mia.com"  # 用户名
mail_pass = "Welc0me12"  # 密码(这里的密码不是登录邮箱密码，而是授权码)

sender = 'system_remind@mia.com'  # 发件人邮箱
# receivers = ['cuijiabin@mia.com']  # 接收人邮箱
receivers = ['cuijia_bin@126.com']  # 接收人邮箱

content = '邮件抄送与密送测试'
title = 'BMP与UMS账号变动提醒'  # 邮件主题


def send_tmp_email(bcc):
    message = MIMEMultipart('mixed')
    message['From'] = "{}".format(sender)
    # message['To'] = ",".join([receive_user])
    # message['Bcc'] = ','.join(['cuijiabin@mia.com'])
    message['Subject'] = title

    try:

        text = "亲爱的蜜兔同学，您好\n"
        text += "    您的蜜兔业务专用邮箱已开通"
        text += "\n"
        text += "    对应您的BMP与UMS登录账号也做了调整，登录邮箱后缀名由 @mia.com 变为 @mompick.com\n"
        text += "    登录密码保持不变，请前往对应系统验证新账户名称，如忘记密码可联系王伟重置密码，如出现其他问题请@崔佳彬反馈问题\n"
        text += "    请及时验证，谢谢~"
        text_plain = MIMEText(text, 'plain', 'utf-8')
        message.attach(text_plain)
        # 启用SSL发信, 端口一般是465
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        # 登录验证
        smtpObj.login(mail_user, mail_pass)
        # 发送
        # smtpObj.sendmail(sender, [receive_user], message.as_string())
        # 密送
        smtpObj.sendmail(sender, [bcc], message.as_string())
        print("mail has been send successfully.", bcc)
    except smtplib.SMTPException as e:
        print(e)


if __name__ == '__main__':
    bcc_list = [
        'cuijia_bin@126.com'
    ]
    for bcc in bcc_list:
        send_tmp_email(bcc)
