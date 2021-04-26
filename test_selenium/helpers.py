from env import url, test_email, password_email, charset, password_users, users
import imaplib
import email
import random
import time



def get_email_code():
    """Вытягиваем код из последнего сообщения с помощью библиоеки IMAP"""
    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(test_email.format(""), password_email)    # Выводит список папок в почтовом ящике.
    mail.select("inbox")  # Подключаемся к папке "входящие".
    result, data = mail.uid('search', None, "ALL")  # Выполняет поиск и возвращает UID писем.
    latest_email_uid = data[0].split()[-1]  # Берем UID последнего сообщение
    # print(latest_email_uid)
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')  # Открываем сообщение по UID
    raw_email = data[0][1]
    raw_email_str = raw_email.decode('utf-8')  # Превращаем бинарную переменную в строку
    email_message = email.message_from_string(raw_email_str)
    result_mass = []
    if email_message.is_multipart():    # Получаем тело сообщения
        # rez = email_message.get_payload()[0].get_payload(decode=True).decode('utf-8')
        # print(rez)
        result_mass.append(1)
        for payload in email_message.get_payload():
            body = payload.get_payload(decode=True).decode('utf-8')
            # print(body)
            result_mass.append(body)
            # print(email_message.get_payload())
    else:
        result_mass.append(2)
        body = email_message.get_payload(decode=True).decode('utf-8')
        result_mass.append(body)
        # print(body)
    if result_mass[0] == 1:
        if len(result_mass[1]) > 10:
            print("1 type")
        else:
            print("2 type")
    else:
        print("3 type")
        code = result_mass[1].split(": ")[1]
        return code[:4]


def generation_login(login):
    """Генерируем случайную почту, прибавляя к стандартной рандомные значения"""
    random_string = "+"
    for i in range(random.randint(3, 15)):
        random_string += random.choice(charset)
    print(login.format(random_string))
    return login.format(random_string)


def check_new_message(old_code):
    """Ожидание нового сообщение (Новый код будет отличаться от старого)"""
    new_code = get_email_code()
    while new_code == old_code:
        time.sleep(1)
        new_code = get_email_code()
        print(new_code)
        continue
    return new_code


def registration(wd):
    """Регистрация пользователя с случайным e-mail"""
    old_code = get_email_code()
    wd.get(url + "registration")
    time.sleep(0.5)
    wd.find_element_by_css_selector("div.ant-modal-confirm-btns button:nth-child(2)").click()
    wd.find_element_by_id("reg_username").send_keys(generation_login(test_email))
    wd.find_element_by_id("reg_password").send_keys(password_users)
    wd.find_element_by_id("reg_confirm").send_keys(password_users)
    wd.find_element_by_id("reg_age").send_keys("21")
    wd.find_element_by_id("reg_agreement").click()
    wd.find_element_by_css_selector('button[type="submit"]').click()
    wd.find_element_by_id("login_val0").send_keys(check_new_message(old_code))
    wd.find_element_by_xpath("//button[.='Go to Profile']").click()
    wd.quit()
    return True


def login(wd):
    """Логин в случайного пользователя из списка"""
    old_code = get_email_code()
    wd.get(url + "login")
    time.sleep(0.5)
    wd.find_element_by_css_selector("div.ant-modal-confirm-btns button:nth-child(2)").click()
    wd.find_element_by_id("login_username").send_keys(random.choice(users))
    wd.find_element_by_id("login_password").send_keys(password_users)
    wd.find_element_by_css_selector('button[type="submit"]').click()
    wd.find_element_by_id("login_val0").send_keys(check_new_message(old_code))
    wd.find_element_by_css_selector('button.ant-btn-primary').click()
    if len(wd.find_elements_by_css_selector('span.ant-avatar')) > 0:
        wd.quit()
        return True
    else:
        wd.quit()
        return False


def forgot(wd):
    """Восстановление пароля"""
    old_code = get_email_code()
    wd.get(url + "forgot")
    time.sleep(0.5)
    wd.find_element_by_css_selector("div.ant-modal-confirm-btns button:nth-child(2)").click()
    wd.find_element_by_id("forgot_username").send_keys(random.choice(users))
    wd.find_element_by_css_selector('button.ant-btn-primary').click()
    wd.find_element_by_id("login_val0").send_keys(check_new_message(old_code))
    wd.find_element_by_id("forgot_password").send_keys(password_users)
    wd.find_element_by_id("forgot_confirm").send_keys(password_users)
    wd.find_element_by_css_selector('button.ant-btn-primary').click()
    if len(wd.find_elements_by_xpath('//a[contains(@href,"/login")]')) > 0:
        wd.quit()
        return True
    else:
        wd.quit()
        return False