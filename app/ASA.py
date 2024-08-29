import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,Toplevel
import os
from tkinter import ttk
from pathlib import Path
import cv2
from PIL import Image, ImageTk
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import numpy as np
import socket
import pickle
import struct
import threading
import time
# from detect_track_yolov7_v2 import setting_model,main_detect
from detect_track_yolov8_v2 import tracking_person,visualize
from business.count.count import counter,draw_line
from tkinter import filedialog
from pymongo.mongo_client import MongoClient
import webbrowser
import subprocess
import platform
import ast
import pygame
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import json

# MongoDB connection URI
uri = "mongodb+srv://13546htl:pT1lNyKREprRYDk4@asa.ydtutxt.mongodb.net/?retryWrites=true&w=majority&appName=ASA"

# Create a new client and connect to the server
client = MongoClient(uri)
# MIN_CANVAS_WIDTH = 1080
# MIN_CANVAS_HEIGHT = 720
# Access the database and collection1
my_db = client["user_data"]
my_col = my_db["user_collection"]

MIN_CANVAS_WIDTH = 1080
MIN_CANVAS_HEIGHT = 720


class StartPage(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("ASA")
        # self.resizable(False, False)
        self.geometry("1080x720")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.verification_code = ""
        global it
        it = 5
        self.width, self.height = 1080, 720
        global is_start
        is_start= True

        # Load the background image
        background_path = 'assets/frame0/startpage_2.jpg'
        logo_path="assets/frame0/logo_1.png"
        # background_path = Path(background_path).as_posix()
        # print(background_path)
        self.image_item = cv2.imread(background_path)
        self.image_logo = cv2.imread(logo_path)
        self.update_background_image()

        # self.logo = tk.PhotoImage(file="assets/frame0/logo_1.png")
        # # self.width_logo,self.height_logo= self.logo.width(),self.logo.height()
        # self.logo_lable = tk.Label(self, image=self.logo ,bg="#000043")
        
        
        self.forget_password = tk.Button(self,text="Quên mật khẩu",bg="#00064a",font=("Helvetica", 14),fg="white",borderwidth=0,highlightthickness=0,command=self.forget_pass)
        self.button_signin_label = tk.Button(self,text="Đăng nhập",bg="#01a1ff",borderwidth=0,highlightthickness=0,font=("Helvetica", 14),command=self.check_user)
        self.button_signup_label = tk.Button(self, text="Đăng ký", bg="#01a1ff",fg="white",borderwidth=0,highlightthickness=0,font=("Helvetica", 14),command=self.register)
        # self.button_signin_label.place(x=x_signin, y=y_signin)

        
        file_path = 'assets/setting/users.json'

        self.entry_user = tk.Entry(self, font=("Helvetica", 14), bd=2, relief=tk.FLAT, insertbackground="black", justify=tk.CENTER ,bg="#6a7394")
        self.entry_pass = PasswordEntry(self, font=("Helvetica", 14), bd=2, relief=tk.FLAT, insertbackground="black", justify=tk.CENTER ,bg="#6a7394")

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    login_data = [json.loads(line) for line in f]
                    if login_data:
                        last_login = login_data[-1]  # Get the most recent login entry
                        self.entry_user.insert(0, last_login['username'])
                        self.entry_pass.insert(0, last_login['password'])
                except json.JSONDecodeError:
                    print("Error decoding JSON from the file.")
        else:
            self.entry_user.insert(0, "Nhập tài khoản")
            self.entry_pass.insert(0, "            ")

        self.entry_user.bind("<Return>", self.on_enter_pressed)
        self.entry_pass.bind("<Return>", self.on_enter_pressed)


        self.place_button_on_startpage()
        # Bind resize event
        self.bind("<Configure>", self.on_root_resize)


    def update_background_image(self):
        resized_image = cv2.resize(self.image_item, (self.width, self.height))
        image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_item_rgb)
        self.background_photo = ImageTk.PhotoImage(image=image_pil)
        if hasattr(self, "background_label"):
            self.background_label.config(image=self.background_photo)
        else:
            # print("cc")
            self.background_label = tk.Label(self, image=self.background_photo)
            self.background_label.place(x=0, y=0)

    def place_button_on_startpage(self):
        # # width_logo,height_logo = self.width/7,self.height/7
        # resized_image = cv2.resize(self.image_logo, (int(self.width/7), int(self.width/7)))
        # image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        # image_pil = Image.fromarray(image_item_rgb)
        # self.logo_photo = ImageTk.PhotoImage(image=image_pil)
        # if hasattr(self, "logo_label"):
        #     self.logo_label.config(image=self.logo_photo)
        #     self.logo_label.place(x=(self.width)*0.5,y=(self.height)*0.25,anchor="center")
        # else:
        #     # print("cc")
        #     self.logo_label = tk.Label(self, image=self.logo_photo,borderwidth=0,highlightthickness=0,bg="#010042")
            # self.logo_label.place(x=(self.width)*0.5,y=(self.height)*0.25)
        # self.logo_lable.place(x=(self.width)*0.5,y=(self.height)*0.25,anchor=tk.CENTER)

        width,height = self.width/6,self.height/18
        width_2,height_2 = self.width/9,self.height/23

        self.entry_user.place(x=(self.width)*0.41,y=(self.height)*0.45,width=width, height=height)
        self.entry_pass.place(x=(self.width)*0.41,y=(self.height)*0.56,width=width, height=height)
        self.button_signin_label.place(x=(self.width)*0.41,y=(self.height)*0.66,width=width, height=height)
        
        self.button_signup_label.config(font=("Helvetica",int(self.width*0.012)))
        self.button_signin_label.config(font=("Helvetica",int(self.width*0.012)))
        self.forget_password.config(font=("Helvetica",int(self.width*0.010)))
        self.entry_user.config(font=("Helvetica",int(self.width*0.012)))
        self.entry_pass.config(font=("Helvetica",int(self.width*0.012)))
        # print(self.width*0.02)
        self.button_signup_label.place(x=(self.width)*0.552,y=(self.height)*0.39, height=height_2)
        self.forget_password.place(x=(self.width)*0.40,y=(self.height)*0.39,width=width_2, height=height_2)



    def forget_pass(self):
        def submit():
            user_name = entry_user_name.get()
            email = entry_email.get()

            # Check if any field is empty
            if not user_name  or not email :
                messagebox.showerror("Lỗi", "Tất cả các thông tin đều bắt buộc.")
                return forget_password_window.lift()
            # Validate username format
            if not self.validate_username(user_name):
                messagebox.showerror("Lỗi", "Tên người dùng phải có từ 4 đến 20 ký tự và chỉ có thể chứa các ký tự chữ và số và dấu gạch dưới.")
                return forget_password_window.lift()
            # Check email format
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                messagebox.showerror("Lỗi", "Vui lòng nhập địa chỉ email hợp lệ.")
                return forget_password_window.lift()

            # Retrieve and print all documents in the collection
            check_user= False
            for document in my_col.find():
                # print(document)
                if user_name == document["user_name"] and email == document["email"]:
                    check_user=True
                    break
            if not check_user:
                messagebox.showerror("lỗi", f"Email và tên tài khoản không chính xác")
                return forget_password_window.lift()
            # Generate verification code and send email
            self.verification_code = self.generate_verification_code()
            self.send_email_forgot_pass(email,user_name, self.verification_code)

            # Prompt user to enter verification code
            verify_window = tk.Toplevel(forget_password_window)
            verify_window.title("Account")
            x = self.forget_password.winfo_rootx()
            y = self.forget_password.winfo_rooty()
            verify_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
            verify_window.geometry(f"+{x-50}+{y}")

            tk.Label(verify_window, text=f"Nhập mã xác nhận đã được gửi đến {email}:").grid(row=0, column=0, padx=10, pady=5)
            entry_verification_code = tk.Entry(verify_window)
            entry_verification_code.grid(row=0, column=1, padx=10, pady=5)
            def verify_code():
                entered_code = entry_verification_code.get()
                if entered_code == self.verification_code:
                    # Prompt user to enter verification code
                    new_password_window = tk.Toplevel(forget_password_window)
                    new_password_window.title("Account")
                    x = self.forget_password.winfo_rootx()
                    y = self.forget_password.winfo_rooty()
                    new_password_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
                    new_password_window.geometry(f"+{x-50}+{y}")

                    tk.Label(new_password_window, text=f"Mật khẩu mới:").grid(row=0, column=0, padx=10, pady=5)
                    new_pass = tk.Entry(new_password_window)
                    new_pass.grid(row=0, column=1, padx=10, pady=5)
                    tk.Label(new_password_window, text=f"Nhập lại mật khẩu:").grid(row=1, column=0, padx=10, pady=5)   
                    new_pass_2 = tk.Entry(new_password_window)
                    new_pass_2.grid(row=1, column=1, padx=10, pady=5)   
                    # Function to update password
                    def update_password(user_name,new_password):
                        result = my_col.update_one({"user_name": user_name}, {"$set": {"password": new_password}})
                        if result.modified_count > 0:
                            messagebox.showinfo("Thành công","Đổi mật khẩu thành công.")
                            new_password_window.destroy()
                            verify_window.destroy()
                            forget_password_window.destroy()
                            # new_password_window.lift()   
                        else:
                            messagebox.showerror("lỗi","mật khẩu trùng với mật khẩu cũ.")
                            new_password_window.lift()
                    def defi_pass():
                        # Validate password format
                        if not self.validate_password(new_pass.get()):
                            messagebox.showerror("Lỗi", "Mật khẩu phải dài ít nhất 8 ký tự, ít nhất 1 chữ cái hoa và 1 chữ thường .")
                            return new_password_window.lift()
                        user_name=entry_user_name.get()  
                        if new_pass.get() == new_pass_2.get():
                            update_password(user_name,new_pass.get())
                        else:
                            messagebox.showerror("Lỗi","Nhập lại mật khẩu xác nhận chưa đúng.")
                            new_password_window.lift()             
                    tk.Button(new_password_window, text="Tiếp tục", command=defi_pass).grid(row=2, columnspan=2, pady=10)        
                    
                else:
                    messagebox.showerror("Activation Error", "Sai mã xác nhận.")
                    verify_window.lift()
            tk.Button(verify_window, text="Verify", command=verify_code).grid(row=1, columnspan=2, pady=10)
        x = self.forget_password.winfo_rootx()
        y = self.forget_password.winfo_rooty()

        forget_password_window = tk.Toplevel(self)
        # register_window.wm_overrideredirect(True)
        forget_password_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
        forget_password_window.geometry(f"+{x-150}+{y}")
        forget_password_window.resizable(False,False)
        forget_password_window.title("forgot password")

        tk.Label(forget_password_window, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=5)
        entry_user_name = tk.Entry(forget_password_window)
        entry_user_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(forget_password_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        entry_email = tk.Entry(forget_password_window)
        entry_email.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(forget_password_window, text="Enter", command=submit).grid(row=4, columnspan=2, pady=10)



    def check_user(self):
        # Retrieve and print all documents in the collection
        check_user= False
        user_name=self.entry_user.get()
        password=self.entry_pass.get()
        for document in my_col.find():
            # print(document)
            if user_name == document["user_name"] and password == document["password"]:
                global user
                user=document
                # print(user["count"])
                check_user=True
        if check_user:
            self.destroy()
            app=PageOne()
            app.mainloop()
            # Assuming self.entry_user.get() and self.entry_pass.get() retrieve username and password
            login_data = {
                "username": user_name,
                "password": password
            }

            file_path = 'assets/setting/users.json'

            # Check if the file exists
            if not os.path.exists(file_path):
                # If the file doesn't exist, create an empty file
                with open(file_path, 'w') as f:
                    pass  # This will create an empty file

            # Open the JSON file in append mode and write the data
            with open(file_path, 'w') as f:
                json.dump(login_data, f)
                f.write('\n')
        else:
            messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu sai")



    # def on_entry_email_click(self,event):
    #     self.entry_user.delete(0, tk.END)  # Clear the default text when the user clicks on the entry box
    # def on_entry_password_click(self,event):
    #     self.entry_pass.delete(0, tk.END)  # Clear the default text when the user clicks on the entry box
    def on_enter_pressed(self,event):
        self.check_user()
      
    def on_root_resize(self, event):
        self.width = max(self.winfo_width(), MIN_CANVAS_WIDTH)
        # print(self.width)
        self.height = max(self.winfo_height(), MIN_CANVAS_HEIGHT)
        self.update_background_image()
        self.place_button_on_startpage()
    def on_closing(self):
        if messagebox.askokcancel("Quit", "bạn muốn tắt ứng dụng bây giờ?"):
            self.destroy()

    # Function to generate a random verification code
    def generate_verification_code(self):
        return str(random.randint(100000, 999999))

    def send_email(self,to_email,user_name,verification_code):
        email='asa.cskh@gmail.com'
        password='vvbg wcru hrgy gpln'
        
        subject = "Chào mừng bạn đến với ASA – Xác nhận email đăng ký!"
        # body = f"Your verification code is: {verification_code}"
        body = f"""\
Dear {user_name},

Cảm ơn bạn đã đăng ký với ASA app! Để hoàn tất quá trình đăng ký, vui lòng sử dụng mã xác minh sau đây:

Verification Code: {verification_code}

Vui lòng nhập mã này để xác minh địa chỉ email và kích hoạt tài khoản của bạn. Nếu bạn không phải là người đăng ký, vui lòng bỏ qua email này.

Nếu bạn gặp bất kỳ vấn đề nào hoặc cần hỗ trợ thêm, đừng ngần ngại liên hệ đội ngũ hỗ trợ qua địa chỉ email {email}.


Best regards,
ASA Team
            """
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(email, password)  
        text = msg.as_string()
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(email, to_email, text)
        #server_ssl.quit()
        server_ssl.close()
        # print ('successfully sent the mail')
    # Global variable to store the verification code


    def send_email_forgot_pass(self,to_email,user_name,verification_code):
        email='asa.cskh@gmail.com'
        password='vvbg wcru hrgy gpln'
        
        subject = "Đặt lại mật khẩu cho tài khoản ASA app!"
        # body = f"Your verification code is: {verification_code}"
        body = f"""\
Dear {user_name},

Bạn đang thực hiện đặt lại mật khẩu cho tài khoản ASA, vui lòng sử dụng mã xác minh sau đây  :

Verification Code: {verification_code}

Vui lòng nhập mã xác nhận bên dưới để hoàn tất quá trình đặt lại mật khẩu tài khoản của bạn. Nếu bạn không phải là người thực hiện, vui lòng bỏ qua email này.

Nếu bạn gặp bất kỳ vấn đề nào hoặc cần hỗ trợ thêm, đừng ngần ngại liên hệ đội ngũ hỗ trợ qua địa chỉ email {email}.


Best regards,
ASA Team
"""
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(email, password)  
        text = msg.as_string()
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(email, to_email, text)
        #server_ssl.quit()
        server_ssl.close()
        # print ('successfully sent the mail')
    # Global variable to store the verification code
    def validate_username(self,username):
        # Check if username is between 4 and 20 characters
        if len(username) < 4 or len(username) > 20:
            return False
        
        # Check if username contains only alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        
        return True
    # Function to validate password format
    def validate_password(self,password):
        # Check if password is at least 8 characters long
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        
        return True
    def register(self):
        def submit():

            user_name = entry_user_name.get()
            password = entry_password.get()
            email = entry_email.get()
            phone = entry_phone.get()

            # Check if any field is empty
            if not user_name or not password or not email or not phone:
                messagebox.showerror("Lỗi", "Tất cả các thông tin đều bắt buộc.")
                return register_window.lift()
            # Validate username format
            if not self.validate_username(user_name):
                messagebox.showerror("Lỗi", "Tên người dùng phải có từ 4 đến 20 ký tự và chỉ có thể chứa các ký tự chữ và số và dấu gạch dưới.")
                return register_window.lift()
            # Validate password format
            if not self.validate_password(password):
                messagebox.showerror("Lỗi", "Mật khẩu phải dài ít nhất 8 ký tự, ít nhất 1 chữ cái hoa và 1 chữ thường .")
                return register_window.lift()
            # Check email format
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                messagebox.showerror("Lỗi", "Vui lòng nhập địa chỉ email hợp lệ.")
                return register_window.lift()
            
            # Check phone format
            phone_regex = r'^\+?\d{10,15}$'  # Allows optional '+' and 10 to 15 digits
            if not re.match(phone_regex, phone):
                messagebox.showerror("Lỗi", "Vui lòng nhập số điện thoại hợp lệ (10-15 chữ số, tùy chọn dấu '+' ở đầu).")
                return register_window.lift()
            # Retrieve and print all documents in the collection
            check_user= False
            check_email = False
            user_regis = ""
            for document in my_col.find():
                # print(document)
                if user_name == document["user_name"]:
                    check_user=True
                    break
                if email == document["email"]:
                    check_email=True
                    user_regis= document["user_name"]
                    break
            if check_user:
                messagebox.showerror("Lỗi", f"{user_name} đã đăng ký trước đó")
                return register_window.lift()
            if check_email:
                messagebox.showerror("Lỗi", f"{email} đã được đăng ký với tên {user_regis}")
                return register_window.lift()
            # Generate verification code and send email
            self.verification_code = self.generate_verification_code()
            self.send_email(email,user_name, self.verification_code)

            # Prompt user to enter verification code
            verify_window = tk.Toplevel(register_window)
            verify_window.title("Activate Account")
            x = self.button_signup_label.winfo_rootx()
            y = self.button_signup_label.winfo_rooty()
            verify_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
            verify_window.geometry(f"+{x-50}+{y}")

            tk.Label(verify_window, text=f"Nhập mã xác nhận đã được gửi đến {email}:").grid(row=0, column=0, padx=10, pady=5)
            entry_verification_code = tk.Entry(verify_window)
            entry_verification_code.grid(row=0, column=1, padx=10, pady=5)
            # Get the current timestamp
            timestamp = time.time()
            # Convert timestamp to a structured time tuple
            time_struct = time.localtime(timestamp)
            # Format the structured time tuple into a readable string
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
            my_dict = {"user_name": f"{user_name}", "password": f"{password}", "ngay-dangky": f"{formatted_time}" ,"email":f"{email}","sdt": f"{phone}","Goi":" Thang","tracking": False ,"count": False , "prowling": False }

            def verify_code():
                entered_code = entry_verification_code.get()
                if entered_code == self.verification_code:
                    messagebox.showinfo("thành công", "Đăng ký tài khoản thành công!")
                    my_col.insert_one(my_dict)
                    verify_window.destroy()
                else:
                    messagebox.showerror("lỗi", "Sai mã xác nhận.")

            tk.Button(verify_window, text="Verify", command=verify_code).grid(row=1, columnspan=2, pady=10)
        x = self.button_signup_label.winfo_rootx()
        y = self.button_signup_label.winfo_rooty()

        register_window = tk.Toplevel(self)
        # register_window.wm_overrideredirect(True)
        register_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
        register_window.geometry(f"+{x-150}+{y}")
        register_window.resizable(False,False)
        register_window.title("Register")

        tk.Label(register_window, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=5)
        entry_user_name = tk.Entry(register_window)
        entry_user_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Mật khẩu:").grid(row=1, column=0, padx=10, pady=5)
        entry_password = tk.Entry(register_window, show="*")
        entry_password.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        entry_email = tk.Entry(register_window)
        entry_email.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(register_window, text="số điện thoại:").grid(row=3, column=0, padx=10, pady=5)
        entry_phone = tk.Entry(register_window)
        entry_phone.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(register_window, text="Register", command=submit).grid(row=4, columnspan=2, pady=10)

class PasswordEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, show="*", **kwargs)


class PageOne(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("ASA")
        # self.resizable(False, False)
        self.geometry("1080x720")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.width, self.height = 1080, 720

        global list_select_index
        list_select_index = []
        self.is_running=False
        self.stop_event = threading.Event()
        global lines,polygon
        lines=[]
        # self.user=user
        # print(self.user)
        polygon=[]
        self.is_cam=1

        background_path = 'assets/frame0/Icon/Asset 32.png'
        # background_path = Path(background_path).as_posix()
        # print(background_path)
        self.image_item = cv2.imread(background_path)
        self.update_background_image()
        self.frame_item = cv2.imread('assets/frame0/banner_1.jpg')
        image_pil = Image.fromarray(self.frame_item)
        self.frame_photo = ImageTk.PhotoImage(image=image_pil)
        self.ismulticam=False
        # Load icons
        self.icons = {}
        self.icons_resize={}
        self.icons_resize_small={}
        
        # print(self.icons)
        self.lines_coor=[]
        self.polygon_coor=[]
        self.load_icons()
        for name,icon in self.icons.items():
            self.icons_resize[name]= self.icon_resize(icon)
        for name,icon in self.icons.items():
            self.icons_resize_small[name]= self.icon_resize_small(icon)
        
        self.back_button = tk.Button(self, image=self.icons_resize["home"], bg="#212529", borderwidth=0, highlightthickness=0, command=self.back_function)

        self.rtsp_list = self.read_from_file('assets/rtsp/rtsp.txt')
        self.name_cam_list = self.read_from_file('assets/rtsp/rtsp_name.txt')
        # self.rtsp_list,self.name_cam_list=self.read_from_rtsp_file('assets/rtsp/rtsp.txt')
        global rtsp_selected
        rtsp_selected = []
        global rtsp_vars
        rtsp_vars = [tk.BooleanVar() for _ in self.rtsp_list]
        # self.previous_states = [0] * len(self.rtsp_list)

        self.rtsp_button = tk.Button(self, image=self.icons_resize["rtsp"], bg="#212529", borderwidth=0, highlightthickness=0, command=self.show_rtsp)
        self.class_list = self.read_from_file('assets/model/class.txt')
        global classes
        classes=[tk.BooleanVar() for _ in self.class_list]
        self.class_button =tk.Button(self, image=self.icons_resize["class"], borderwidth=0, highlightthickness=0, bg="#212529",command=self.show_class)
        self.options_function= ["tracking","count","prowling"]

        global option_function
        option_function=[tk.BooleanVar() for _ in self.options_function]
        self.function_button =tk.Button(self, image=self.icons_resize["function"], borderwidth=0, highlightthickness=0, bg="#212529",command=self.show_function)
        self.setting_button =tk.Button(self, image=self.icons_resize["setting"], bg="#212529", borderwidth=0, highlightthickness=0,command=self.save_all_state)


        self.play_button =tk.Button(self, image=self.icons_resize["play"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.play_function)
        self.prev_button =tk.Button(self, image=self.icons_resize["prev"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.prev_function)
        self.stop_button =tk.Button(self, image=self.icons_resize["stop"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.stop_function)
        self.next_button =tk.Button(self, image=self.icons_resize["next"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.next_function)
        self.multicam_button =tk.Button(self, image=self.icons_resize["multicam"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.multicam_function)

        self.file_button =tk.Button(self, image=self.icons_resize["file"],bg="#0B0F1A", borderwidth=0, highlightthickness=0,command=self.open_folder)

        self.show_class()
        self.show_rtsp()
        self.check_display()
        self.show_function()

        self.trangchu_button = tk.Button(self, text=" Website chúng tôi ", command=self.open_website)
        global  chk_nolabel_button,chk_nolabel,chk_nobox,chk_nobox_button ,chk_show_fps,chk_show_fps_button
        

        global chk_unique_track_color,chk_unique_track_color_button
        chk_unique_track_color = tk.BooleanVar()
        chk_unique_track_color.set(False)  
        chk_unique_track_color_button = tk.Checkbutton(self, text="unique track color",fg= "black", variable=chk_unique_track_color, state=tk.DISABLED)

        chk_nolabel = tk.BooleanVar()
        chk_nolabel.set(False)  
        chk_nolabel_button = tk.Checkbutton(self, text="No Label          ",fg= "black", variable=chk_nolabel)

        chk_nobox = tk.BooleanVar()
        chk_nobox.set(False)  
        chk_nobox_button = tk.Checkbutton(self, text="No Box            ",fg= "black", variable=chk_nobox)

        chk_show_fps = tk.BooleanVar()
        chk_show_fps.set(True)  
        chk_show_fps_button = tk.Checkbutton(self, text="show fps          ",fg= "black", variable=chk_show_fps)

        global chk_agnostic_nms,chk_agnostic_nms_button,chk_augment,chk_augment_button
        chk_augment = tk.BooleanVar()
        chk_augment.set(False)  
        chk_augment_button = tk.Checkbutton(self, text="augment           ",fg= "black", variable=chk_augment)

        chk_agnostic_nms = tk.BooleanVar()
        chk_agnostic_nms.set(False)  
        chk_agnostic_nms_button = tk.Checkbutton(self, text="agnostic nms      ",fg= "black", variable=chk_agnostic_nms)

        global conf_thres_str , conf_thres
        conf_thres_str = tk.StringVar()
        conf_thres = tk.Entry(self, textvariable=conf_thres_str, width=10)
        conf_thres.insert(0, "conf thres")

        global iou_thres_str , iou_thres
        iou_thres_str = tk.StringVar()
        iou_thres = tk.Entry(self, textvariable=iou_thres_str, width=10)
        iou_thres.insert(0, "iou thres")

        global weight_str , weight
        weight_str = tk.StringVar()
        weight = tk.Entry(self, textvariable=weight_str, width=10)
        weight.insert(0, "last.pt")
        global is_cam,is_file
        is_file,is_cam = False,False

        self.load_state()
        self.define_var()

        self.bind("<Configure>", self.on_resize)
    def on_closing(self):
        if messagebox.askokcancel("Tắt", "Tắt ứng dụng?"):
            self.destroy()
    def back_function(self):
        if messagebox.askokcancel("Quay lại", "Quay lại trang đầu?"):
            self.stop_event.is_set()
            self.destroy()
            app= StartPage()
            app.mainloop()
    def check_display(self):
        self.frame_label = tk.Label(self, image=self.frame_photo,highlightthickness=0,borderwidth=0)
        self.update_size()
    def multicam_function(self):
        if not self.ismulticam:
            self.frame_label_1 = tk.Label(self, image=self.frame_photo,highlightthickness=0,borderwidth=0)
            self.frame_label_2 = tk.Label(self, image=self.frame_photo,highlightthickness=0,borderwidth=0)
            self.frame_label_3 = tk.Label(self, image=self.frame_photo,highlightthickness=0,borderwidth=0)
            self.frame_label_4 = tk.Label(self, image=self.frame_photo,highlightthickness=0,borderwidth=0)
            self.ismulticam=True
            self.frame_label.destroy()
            del self.frame_label
            # self.frame_label.place(x=(self.width)*0.555, y=self.height*0.468,anchor="center")
        else:
            self.frame_label = tk.Label(self, image=self.frame_photo,highlightthickness=0,borderwidth=0)
            self.ismulticam=False
            self.frame_label_1.destroy()
            self.frame_label_2.destroy()
            self.frame_label_3.destroy()
            self.frame_label_4.destroy()
            del self.frame_label_1
            del self.frame_label_2
            del self.frame_label_3
            del self.frame_label_4
        # if self.is_running:
        #     self.stop_event.set()
        #     self.play_function()
        self.update_size()
    def play_warning_sound(self):
        pygame.mixer.init()
        alert_sound = pygame.mixer.Sound('assets/sound/beep-warning-6387.mp3')  # Replace with your sound file path
        alert_sound.play()
    def load_state(self):
        if os.path.exists("assets/setting/setting.txt"):
            with open("assets/setting/setting.txt", "r") as file:
                states = file.readlines()
                for idx, state in enumerate(states):
                    if state.startswith("rtsp"):
                        state_dict = eval(state.strip()[5:])
                        for rtsp, selected in state_dict.items():
                            if rtsp in self.rtsp_list:
                                idx = self.rtsp_list.index(rtsp)
                                value = True if selected else False
                                rtsp_vars[idx].set(value)
                    elif state.startswith("class"):
                    #     rtsp_vars[idx].set(True)
                        state = state.replace("class ", "").replace(":", "").strip()
                        # print(state)
                        name, value = state.split()
                        value = value.lower() == 'true'
                        if name in self.class_list:
                            idx = self.class_list.index(name)
                            classes[idx].set(value)

                    elif state.startswith("function"):
                        state = state.replace("function ", "").replace(":", "").strip()
                        # print(state)
                        name, value = state.split()
                        if name == "prowling":
                            if user["prowling"]:
                                value = value.lower() == 'true'
                                # print(value)
                                if name in self.options_function:
                                    # print(name)
                                    idx = self.options_function.index(name)
                                    option_function[idx].set(value)
                                    continue
                        elif name == "count":
                            if user["count"]:
                                value = value.lower() == 'true'
                                # print(value)
                                if name in self.options_function:
                                    # print(name)
                                    idx = self.options_function.index(name)
                                    option_function[idx].set(value)
                                    continue
                        elif name == "tracking":
                            if user["tracking"]:
                                value = value.lower() == 'true'
                                # print(value)
                                if name in self.options_function:
                                    # print(name)
                                    idx = self.options_function.index(name)
                                    option_function[idx].set(value)
                                    continue
                        else:
                            value = value.lower() == 'true'
                            # print(value)
                            if name in self.options_function:
                                # print(name)
                                idx = self.options_function.index(name)
                                option_function[idx].set(value)

                    elif state.startswith("line"):
                        state = state.replace("line ", "").strip()
                        # Remove the surrounding quotation marks
                        cleaned_string = state.strip('[]"')
                        # Use ast.literal_eval to safely evaluate the cleaned string
                        result = ast.literal_eval(cleaned_string)
                        self.lines_coor.append(result)
                    elif state.startswith("polygon"):
                        state = state.replace("polygon ", "").strip()
                        # Remove the surrounding quotation marks
                        cleaned_string = state.strip('[]"')
                        # Use ast.literal_eval to safely evaluate the cleaned string
                        result = ast.literal_eval(cleaned_string)
                        self.polygon_coor.append(result)
                    # for key,value in 
                    # state_dict = ast.literal_eval(state.strip())
                    # for rtsp, selected in state_dict.items():
                    #     if rtsp in self.rtsp_list:
                    #         idx = self.rtsp_list.index(rtsp)
                    #         value = True if selected else False
                    #         rtsp_vars[idx].set(value)

    def save_all_state(self):
        self.define_var()
        file_path = 'assets/setting/setting.txt'
        # Check if the file exists
        if not os.path.exists(file_path):
            # If the file doesn't exist, create an empty file
            with open(file_path, 'w') as f:
                pass  # This will create an empty file

        with open("assets/setting/setting.txt", "w") as file:
            # print(self.classes_check)
            # print(self.options_check)
            # print(self.rtsp_check)
            # print(self.lines_coor)
            for var in self.rtsp_check:
                file.write(f"rtsp {var}\n")
            for key,value in self.classes_check.items():
                # print(key)
                file.write(f'class {key}: {value}\n')
            for key,value in self.options_check.items():
                file.write(f'function {key}: {value}\n')
                # file.write(f"function {var}\n")
            for var in self.lines_coor:
                file.write(f"line {var}\n")
            for var in self.polygon_coor:
                file.write(f"polygon {var}\n")


    def define_var(self):
        # self.classes_check=[]
        self.rtsp_check=[]
        # self.options_check=[]
        # for idx, item in enumerate(self.options_function):
        #     option={item: option_function[idx].get()}
        #     self.options_check.append(option)
        # for idx,item in enumerate(self.class_list):
        #     option={item: classes[idx].get()}
        #     self.classes_check.append(option)
        for idx, rtsp_item in enumerate(self.rtsp_list):
            option={rtsp_item: rtsp_vars[idx].get()}
            self.rtsp_check.append(option)

        # self.options_check = {k.lower(): v for d in self.options_check for k, v in d.items()}
        # self.rtsp_check = {k.lower(): v for d in self.rtsp_check for k, v in d.items()}
        # self.classes_check = {k.lower(): v for d in self.classes_check for k, v in d.items()}


        self.classes_check={}
        # self.rtsp_check={}
        self.options_check={}
        for idx, item in enumerate(self.options_function):
            self.options_check[item.lower()] = option_function[idx].get()
            
        for idx,item in enumerate(self.class_list):
            self.classes_check[item.lower()] = classes[idx].get()
            if not classes[idx].get() and idx in list_select_index:
                list_select_index.remove(idx)
            if classes[idx].get() and idx not in list_select_index:
                list_select_index.append(idx)
        # for idx, rtsp_item in enumerate(self.rtsp_list):
        #     self.rtsp_check[rtsp_item.lower()] = rtsp_vars[idx].get()
        # print(list_select_index)
        global rtsp_selected
        rtsp_selected = [key for d in self.rtsp_check for key, value in d.items() if value is True]
        global info_cams
        info_cams=[]
        for i,item in enumerate(self.rtsp_list):
            name_cam=f"cam_{i}"
            info_cam = {
                name_cam:{
                "rtsp": item,
                "port": i + 1,
                "line_name": f"line_cam_{i}",
                "polygon_name": f"polygon_cam_{i}",
                "is_select": rtsp_vars[i].get() 
            }}
            info_cams.append(info_cam)
        for var in lines:
            for value in var.lines:
                if value not in self.lines_coor:
                    # print(value)
                    self.lines_coor.append(value)
        lines.clear()
        for var in polygon:
            for value in var.polygons:
                if value not in self.polygon_coor:
                    # print(value)
                    self.polygon_coor.append(value)
        polygon.clear()
    def prev_function(self):
        self.define_var()
        if self.is_cam>1 :
            self.is_cam -=1
    def next_function(self):
        self.define_var()
        if self.is_cam<4 and self.is_cam<=len(rtsp_selected)+1:
            self.is_cam +=1
    def stop_function(self):
        self.stop_event.set()
        self.is_running=False
        self.stop_button.place_forget() 
        self.play_button.place_configure(x=(self.width)*0.53,y=self.height * 0.88)
    def play_function(self):
        
        self.define_var()
        index_cam = 1
        # print(rtsp_selected)
        if len(rtsp_selected)>0:
            self.is_running=True
            global server_thread, tracking_thread
            self.stop_event.clear()
            # print(info_cams)
            
            for i,info_cam in enumerate(info_cams):
                if info_cam[f"cam_{i}"]["rtsp"] in rtsp_selected:
                    # print(info_cam)
                    # idx= rtsp_selected.index(info_cam[f"cam_{i}"]["rtsp"])
                    server_thread = threading.Thread(target=self.read_frame,args=( info_cam[f"cam_{i}"]["rtsp"], info_cam[f"cam_{i}"]["port"]))
                    server_thread.daemon = True
                    server_thread.start()
                    time.sleep(5)
                    tracking_thread = threading.Thread(target=self.run_tracking_test,args= ('127.0.0.1', info_cam[f"cam_{i}"]["port"],index_cam))
                    tracking_thread.daemon = True
                    tracking_thread.start()
                    # time.sleep(2)
                    index_cam+=1
            # print(self.rtsp_check)
            # print(self.classes_check)
            # print(self.options_check["tracking"])
            self.play_button.place_forget() 
            self.stop_button.place_configure(x=(self.width)*0.53,y=self.height * 0.88)
        else:
            messagebox.showerror("lỗi","bạn chưa chọn cam để chạy")
            # print(info_cams)


    def read_frame(self ,rtsp,port):
        if rtsp == "0":
            rtsp = 0
        # print(rtsp)
        cap = cv2.VideoCapture(rtsp)
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to a host and port
        host = '0.0.0.0'  # Use '0.0.0.0' to bind to all available interfaces
        server_socket.bind((host, port))
        # Listen for incoming connections
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        i = 0
        while True:
            # print(stop_event)
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            try:
                while True:
                    # print(self.stop_event)
                    ret, frame = cap.read()
                    i +=1 
                    if i % 4 ==0:
                        if not ret:
                            print("Error: Could not read frame.")
                            cap = cv2.VideoCapture(rtsp)
                            continue
                        frame=frame[::3,::3]
                        data = pickle.dumps(frame)
                        client_socket.sendall(struct.pack("<L", len(data)))
                        client_socket.sendall(data)
                        if self.stop_event.is_set():
                            # print("cc_1")
                            break
                
            except ConnectionResetError:
                print("Connection closed by client.")
            if self.stop_event.is_set():
                # print("cc_2")
                cap.release()
                client_socket.close()
                server_socket.close()
                break


    def run_tracking_test(self, host, port , index):
        # Get the current timestamp
        timestamp = time.time()
        # Convert timestamp to a structured time tuple
        time_struct = time.localtime(timestamp)
        # Format the structured time tuple into a readable string
        formatted_time = time.strftime("%Y-%m-%d_%Hh-%Mm-%Ss", time_struct)
        formatted_date = time.strftime("%Y-%m-%d", time_struct)
        folder_path_warning=f'warning/{formatted_date}'
        folder_path=f'save/{formatted_date}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        else:
            print(f"Folder '{folder_path}' already exists.")
        if not os.path.exists(folder_path_warning):
            os.makedirs(folder_path_warning)
            print(f"Folder '{folder_path_warning}' created.")
        else:
            print(f"Folder '{folder_path_warning}' already exists.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = '127.0.0.1'
        # port = 9999
        client_socket.connect((host, port))
        warning_time=0
        i=0
        warning_obj=False
        coordinates_lists = []
        boudary=[]
        if self.options_check["count"]:
            # Iterate through each tuple in the list
            # for item in lines:
            #     if item.cam_info['port']==port:

            # print(self.lines_coor)
            for line_tuple in self.lines_coor:
                point_set, _ = line_tuple
                if _ == f"line_cam_{port-1}":
                    coordinates = [(x, y) for x, y in point_set]
                    coordinates_lists.append(coordinates)
            line_zones=draw_line(coordinates_lists)

        if self.options_check["prowling"]:
            for polygon_tuple in self.polygon_coor:
                point_set,_=polygon_tuple
                if _== f"polygon_cam_{port-1}":
                    boudary.append(point_set)
            # print(boudary)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # cap = cv2.VideoCapture(source)
        vid_path, output_writers = None, None
        save_path=f'save/{formatted_date}/{formatted_time}_cam_{index}'
        print(save_path)
        while True:

            data = client_socket.recv(4)
            if not data:
                continue
            frame_size = struct.unpack("<L", data)[0]
            data = b""
            while len(data) < frame_size:
                packet = client_socket.recv(frame_size - len(data))
                if not packet:
                    break
                data += packet
            frame = pickle.loads(data)
            objects, fps = tracking_person(frame,self.options_check["tracking"],list_select_index,boudary)
            if len(objects)<=0:
                i+=1
            for obj in objects:
                if self.options_check["tracking"]:
                    if obj["is_in_bound"] :
                        warning_time +=1
                        # print(i)
                        i=0
                    else:
                        i+=1
                    if warning_time >=100:
                        # Get the current timestamp
                        times_time = time.time()
                        # Convert timestamp to a structured time tuple
                        time_time = time.localtime(times_time)
                        warning_time_fomat = time.strftime("%Y-%m-%d_%Hh-%Mm-%Ss", time_time)
                        cv2.imwrite(f'warning/{formatted_date}/frame_{warning_time_fomat}.jpg', frame)
                        self.play_warning_sound()
                        warning_obj=True
                        warning_time=0
                        i=0
                    elif i>=100:
                        warning_time=0
                        i=0
                        warning_obj=False

            # print(list_select_index)
            # print(objects)
            if self.options_check["count"] :
                in_count,out_count = counter(objects,line_zones)
                # cv2.putText(frame, f"In: {in_count}  Out: {out_count}", (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),1)
                # Draw the lines on the image
                for line in coordinates_lists:
                    points = list(line)
                    start_point = points[0]
                    end_point = points[1]
                    cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
            if self.options_check["prowling"] :
                for contour in boudary:
                    contour_array = np.array(contour, dtype=np.int32)
                    cv2.polylines(frame, [contour_array], isClosed=True, color=(0, 255, 0), thickness=5)    
            frame = visualize(frame,objects, self.options_check["tracking"],chk_nolabel.get(),chk_nobox.get(),warning_obj)                       
            if not self.ismulticam:
                if index == self.is_cam:
                    frame = cv2.resize(frame,  (int(self.width*0.748), int(self.height*0.7)))
                    if self.options_check["count"]:
                        cv2.putText(frame, f"In: {in_count}  Out: {out_count}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),1)
                    # cv2.putText(frame, "FPS: " + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
                    img_background = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = ImageTk.PhotoImage(image=Image.fromarray(img_background))
                    self.frame_label.config(image=photo)
                    self.frame_label.image = photo
            else:
                frame = cv2.resize(frame,  (int(self.width * (0.748 / 2)), int(self.height * (0.7 / 2))))
                if self.options_check["count"]:
                    cv2.putText(frame, f"In: {in_count}  Out: {out_count}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),1)
                # cv2.putText(frame, "FPS: " + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
                img_background = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(img_background))
                # for i in range(4):
                #     if port == i + 1:                    
                frame_attr_name = f'frame_label_{index}'
                frame_attr = getattr(self, frame_attr_name)
                frame_attr.config(image=photo) 
                frame_attr.image=photo
            if vid_path != save_path:  # new video
                vid_path = save_path
                if isinstance(output_writers, cv2.VideoWriter):
                    output_writers.release()  # release previous video writer

                else:  # stream
                    save_path += '.mp4'
                output_writers = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'),10, (frame.shape[1], frame.shape[0]))            

            output_writers.write(frame)   
            if self.stop_event.is_set():
                # print("cc")
                client_socket.close()
                break
        output_writers.release()
        cv2.destroyAllWindows()
        # print("dd")
    def show_rtsp(self, event=None):
        # width = 150
        # height = 200
        x = self.rtsp_button.winfo_rootx()
        y = self.rtsp_button.winfo_rooty() + self.function_button.winfo_height()
        checklist_window = tk.Toplevel(self)
        checklist_window.wm_overrideredirect(True)
        checklist_window.configure(bg="#1f2227",borderwidth=1, highlightthickness=2,highlightcolor="white")
        checklist_window.geometry(f"+{x+50}+{y}")
        self.rtsp_checkbuttons = []
        # Frame for buttons
        button_frame = tk.Frame(checklist_window, bg="#1f2227")
        button_frame.pack(fill=tk.X)
        self.is_selectAllRtsp= False
        # Create three buttons

        # self.multicam_button =tk.Button(self, image=self.icons_resize["multicam"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.check_display)
        selectAll_button = tk.Button(button_frame,image=self.icons_resize_small["select_all"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.select_all_rtsp)
        selectAll_button.pack(side=tk.LEFT, padx=2, pady=5)
        add_rtsp_button = tk.Button(button_frame,image=self.icons_resize_small["add"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.open_choice_window)
        add_rtsp_button.pack(side=tk.LEFT,  padx=10, pady=5)
        delete_button = tk.Button(button_frame,image=self.icons_resize_small["delete"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.delete_rtsp)
        delete_button.pack(side=tk.LEFT,  padx=2, pady=5)


        line= tk.Frame(checklist_window, bg="white")
        line.pack(fill=tk.X)

        # print(self.rtsp_list)
        canvas = tk.Canvas(checklist_window, bg="#1f2227", highlightthickness=0,width=150, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a Scrollbar for the Canvas
        scrollbar = tk.Scrollbar(checklist_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)
        # Create a Frame inside the Canvas to hold the Checkbuttons
        frame = tk.Frame(canvas, bg="#1f2227")
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)


        # Populate Checkbuttons
        for idx, item in enumerate(self.rtsp_list):
            # chk_btn = tk.Checkbutton(frame, text=f"{item}", fg="white", selectcolor="#0B0F1A", bg="#1f2227")
            # chk_btn.pack(pady=5, anchor=tk.W)
            info=f"{self.name_cam_list[idx]}"
            chk_btn = tk.Checkbutton(frame, text=info,fg="white", selectcolor="#0B0F1A", variable=rtsp_vars[idx],bg="#1f2227", command=lambda idx=idx: self.check_SL(idx))
            chk_btn.pack(pady=5, anchor=tk.W)
            # chk_btn.place(x=coor_X,y=coor_y)
            # coor_y+=40
            self.rtsp_checkbuttons.append((rtsp_vars[idx],chk_btn))

        # Update the scroll region after widgets are added
        frame.update_idletasks()  # Ensure frame is correctly calculated
        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Set scroll region based on frame size

        # # Destroy checklist_window on FocusOut
        # checklist_window.bind("<FocusOut>", lambda e: checklist_window.destroy())
        # checklist_window.focus_set()
        global is_start
        if is_start:
            checklist_window.destroy()
        else:
            checklist_window.bind("<FocusOut>", lambda e: checklist_window.destroy())
            checklist_window.focus_set()
        # coor_X= 0
        # coor_y=10
        # for idx, rtsp_item in enumerate(self.rtsp_list):
        #     info=f"cam_{idx+1}"
        #     chk_btn = tk.Checkbutton(checklist_window, text=info,fg="white", selectcolor="#0B0F1A", variable=rtsp_vars[idx],bg="#1f2227")
        #     chk_btn.place(x=coor_X,y=coor_y)
        #     coor_y+=40
        #     self.rtsp_checkbuttons.append(chk_btn)
        # global is_start
        # if is_start:
        #     checklist_window.destroy()
        # else:
        #     checklist_window.bind("<FocusOut>", lambda e: checklist_window.destroy())
        #     checklist_window.focus_set()
        
    def check_SL(self, idx):
        self.define_var()
        if len(rtsp_selected) > 4:
            rtsp_vars[idx].set(False)
            messagebox.showerror("lỗi", "Số lượng tối đa là 4 RTSP")
        self.show_rtsp()
    def show_function(self, event=None):
        x = self.rtsp_button.winfo_rootx()
        y = self.rtsp_button.winfo_rooty() + self.function_button.winfo_height()
        checklist_window = Toplevel(self)
        checklist_window.wm_overrideredirect(True)
        checklist_window.configure(bg="#1f2227",borderwidth=1, highlightthickness=2,highlightcolor="white")
        checklist_window.geometry(f"+{x+50}+{y}")
        self.class_checkbuttons = []
        # button2 = tk.Button(button_frame, text="Button 2", fg="white", bg="#444b54")
        # button2.pack(side=tk.LEFT,  padx=0, pady=5)
        # button3 = tk.Button(button_frame, text="Button 3", fg="white", bg="#444b54")
        # button3.pack(side=tk.LEFT,  padx=5, pady=5)
        # # Frame for buttons
        button_frame_1 = tk.Frame(checklist_window, bg="#2f6ecb")
        button_frame_1.pack(fill=tk.X)
        
        draw_line_button = tk.Button(button_frame_1, text="Draw line", fg="white", borderwidth=0, highlightthickness=0,state=tk.DISABLED, bg="#2f6ecb",command=self.draw_line_function)
        draw_line_button.pack(side=tk.LEFT, padx=5, pady=5)

        draw_polygon_button = tk.Button(button_frame_1, text="Draw polygon", fg="white", borderwidth=0, highlightthickness=0,state=tk.DISABLED, bg="#2f6ecb",command=self.draw_polygon_function)
        draw_polygon_button.pack(side=tk.LEFT, padx=5, pady=5)
        if user["prowling"]:
            draw_polygon_button.config(state=tk.NORMAL)
        if user["count"]:
            draw_line_button.config(state=tk.NORMAL)
        line= tk.Frame(checklist_window, bg="white")
        line.pack(fill=tk.X)

        # Frame for buttons
        button_frame = tk.Frame(checklist_window, bg="#1f2227")
        button_frame.pack(fill=tk.X)
        self.is_selectAllfunction= False
        # Create three buttons
        selectAll_button = tk.Button(button_frame,image=self.icons_resize_small["select_all"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.select_all_function)
        selectAll_button.pack(side=tk.LEFT, padx=5, pady=5)
        line_1= tk.Frame(checklist_window, bg="white")
        line_1.pack(fill=tk.X)
        # Create a Canvas widget
        canvas = tk.Canvas(checklist_window, bg="#1f2227", highlightthickness=0,width=150, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Add a Scrollbar for the Canvas
        scrollbar = tk.Scrollbar(checklist_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a Frame inside the Canvas to hold the Checkbuttons
        frame = tk.Frame(canvas, bg="#1f2227")
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        self.option_checkbuttons = []

        for idx, item in enumerate(self.options_function):
            if item == "count":
                if user["count"]:
                    chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                    chk_btn.pack(pady=5, anchor=tk.W)
                    self.option_checkbuttons.append((option_function[idx],chk_btn))
                    continue
                else:
                    chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                    self.option_checkbuttons.append((option_function[idx],chk_btn))
                    continue
            elif item == "prowling":
                if user["prowling"]:
                    chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                    chk_btn.pack(pady=5, anchor=tk.W)
                    self.option_checkbuttons.append((option_function[idx],chk_btn))
                    continue
                else:
                    chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                    self.option_checkbuttons.append((option_function[idx],chk_btn))
            elif item == "tracking":
                if user["tracking"]:
                    chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                    chk_btn.pack(pady=5, anchor=tk.W)
                    self.option_checkbuttons.append((option_function[idx],chk_btn))
                    continue
                else:
                    chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                    self.option_checkbuttons.append((option_function[idx],chk_btn))                      
            else:
                chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", variable=option_function[idx], selectcolor="#0B0F1A",bg="#1f2227",command=self.toggle_track)
                chk_btn.pack(pady=5, anchor=tk.W)
                self.option_checkbuttons.append((option_function[idx],chk_btn))
        self.toggle_track()
        # Update the scroll region after widgets are added
        frame.update_idletasks()  # Ensure frame is correctly calculated
        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Set scroll region based on frame size


        global is_start
        if is_start:
            checklist_window.destroy()
            is_start= False
        else:
            checklist_window.bind("<FocusOut>", lambda e: checklist_window.destroy())
            checklist_window.focus_set()


    def show_class(self, event=None):
        x = self.rtsp_button.winfo_rootx()
        y = self.rtsp_button.winfo_rooty() + self.function_button.winfo_height()
        checklist_window = Toplevel(self)
        checklist_window.wm_overrideredirect(True)
        checklist_window.configure(bg="#1f2227",borderwidth=1, highlightthickness=2,highlightcolor="white")
        checklist_window.geometry(f"+{x+50}+{y}")
        self.class_checkbuttons = []

        # Frame for buttons
        button_frame = tk.Frame(checklist_window, bg="#28292d")
        button_frame.pack(fill=tk.X)
        self.is_selectAllClass= False
        # Create three buttons
        selectAll_button = tk.Button(button_frame,image=self.icons_resize_small["select_all"],bg="#081c3d", borderwidth=0, highlightthickness=0,command=self.select_all_class)
        selectAll_button.pack(side=tk.LEFT, padx=5, pady=5)
        # button2 = tk.Button(button_frame, text="Button 2", fg="white", bg="#444b54")
        # button2.pack(side=tk.LEFT,  padx=0, pady=5)
        # button3 = tk.Button(button_frame, text="Button 3", fg="white", bg="#444b54")
        # button3.pack(side=tk.LEFT,  padx=5, pady=5)

        line= tk.Frame(checklist_window, bg="white")
        line.pack(fill=tk.X)
        # Create a Canvas widget
        canvas = tk.Canvas(checklist_window, bg="#1f2227", highlightthickness=0,width=150, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a Scrollbar for the Canvas
        scrollbar = tk.Scrollbar(checklist_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a Frame inside the Canvas to hold the Checkbuttons
        frame = tk.Frame(canvas, bg="#1f2227")
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        # Populate Checkbuttons
        for idx, item in enumerate(self.class_list):
            # chk_btn = tk.Checkbutton(frame, text=f"{item}", fg="white", selectcolor="#0B0F1A", bg="#1f2227")
            # chk_btn.pack(pady=5, anchor=tk.W)
            chk_btn = tk.Checkbutton(frame, text=f"{item}",fg="white", selectcolor="#0B0F1A", variable=classes[idx],bg="#1f2227")
            chk_btn.pack(pady=5, anchor=tk.W)
            # chk_btn.place(x=coor_X,y=coor_y)
            # coor_y+=40
            self.class_checkbuttons.append((classes[idx],chk_btn))

        # Update the scroll region after widgets are added
        frame.update_idletasks()  # Ensure frame is correctly calculated
        canvas.config(scrollregion=canvas.bbox(tk.ALL))  # Set scroll region based on frame size

        # # Destroy checklist_window on FocusOut
        # checklist_window.bind("<FocusOut>", lambda e: checklist_window.destroy())
        # checklist_window.focus_set()
        global is_start
        if is_start:
            checklist_window.destroy()
        else:
            checklist_window.bind("<FocusOut>", lambda e: checklist_window.destroy())
            checklist_window.focus_set()

    def select_all_class(self):
        if self.is_selectAllClass:
            for var, chk_btn in self.class_checkbuttons:
                var.set(False)
            self.is_selectAllClass =False
        else:
            for var, chk_btn in self.class_checkbuttons:
                var.set(True)
            self.is_selectAllClass = True
    def select_all_rtsp(self):
        self.define_var()
        if self.is_selectAllRtsp:
            for var, chk_btn in self.rtsp_checkbuttons:
                var.set(False)
            self.is_selectAllRtsp =False
        else:
            for idx,(var,chk_btn) in enumerate(self.rtsp_checkbuttons):
                if idx<4:
            # for var, chk_btn in self.rtsp_checkbuttons:
                    var.set(True)
            self.is_selectAllRtsp = True
    def select_all_function(self):
        if self.is_selectAllfunction:
            for var, chk_btn in self.option_checkbuttons:
                var.set(False)
            self.is_selectAllfunction =False
            self.toggle_track()
        else:
            for var, chk_btn in self.option_checkbuttons:
                var.set(True)
            self.is_selectAllfunction = True
            self.toggle_track()
    # def add_rtsp_window(self):
    #     # Create a new Toplevel window for adding RTSP
    #     add_rtsp_window = tk.Toplevel(self)
    #     add_rtsp_window.configure(bg="#1f2227", borderwidth=1, highlightthickness=1)

    #     # Entry widget for RTSP URL
    #     rtsp_entry = tk.Entry(add_rtsp_window, bg="white", fg="black", relief=tk.FLAT)
    #     rtsp_entry.pack(padx=10, pady=10)

    #     # Button to add RTSP URL (dummy functionality)
    #     add_button = tk.Button(add_rtsp_window, text="Add RTSP", fg="white", bg="#444b54",
    #                            command=lambda: self.add_rtsp(rtsp_entry.get()))
    #     add_button.pack(padx=10, pady=5)

    #     # Destroy add_rtsp_window on FocusOut
    #     add_rtsp_window.bind("<FocusOut>", lambda e: add_rtsp_window.destroy())
    #     add_rtsp_window.focus_set()
    def open_choice_window(self):
        choice_window = tk.Toplevel(self)
        choice_window.title("Choose an Option")
        x = self.rtsp_button.winfo_rootx()
        y = self.rtsp_button.winfo_rooty() + self.function_button.winfo_height()
        choice_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
        choice_window.resizable(False,False)
        choice_window.geometry(f"+{x+50}+{y}")
        def add_rtsp( rtsp_url,name_rtsp):
            is_already = False
            for idx, key in enumerate(self.rtsp_list):
                if rtsp_url == key:
                    is_already = True
                    break
            if is_already:
                messagebox.showerror("lỗi", "Bạn đã có RTSP này trước đó")
                choice_window.lift()
            else:
                if rtsp_url == "0":
                    rtsp_url=0
                cap = cv2.VideoCapture(rtsp_url)
                ret, frame = cap.read()
                if not ret:
                    
                    messagebox.showerror("lỗi", "RTSP không hợp lệ")
                    choice_window.lift()
                else:
                    
                    self.rtsp_list.append(str(rtsp_url))
                    rtsp_var = tk.BooleanVar()
                    rtsp_vars.append(rtsp_var)
                    self.name_cam_list.append(str(name_rtsp))
                    self.save_rtsp_list_to_file()
                    messagebox.showinfo("Info", "Thêm RTSP thành công")
                    
                    self.show_rtsp()
        def add_rtsp_window():
            add_rtsp_window = tk.Toplevel(choice_window)
            add_rtsp_window.title("Enter Camera Information")
            add_rtsp_window.resizable(False,False)
            add_rtsp_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
            add_rtsp_window.geometry(f"+{x+50}+{y}")


            # Labels and Entry fields for each piece of information
            tk.Label(add_rtsp_window, text="Tên cam:").grid(row=0, column=0, padx=10, pady=5)
            tk.Label(add_rtsp_window, text="Địa Chỉ IP:").grid(row=1, column=0, padx=10, pady=5)
            tk.Label(add_rtsp_window, text="Mật khẩu(verify code):").grid(row=2, column=0, padx=10, pady=5)
            tk.Label(add_rtsp_window, text="Port:").grid(row=3, column=0, padx=10, pady=5)

            # Entry widgets
            camera_name_entry = tk.Entry(add_rtsp_window)
            ip_address_entry = tk.Entry(add_rtsp_window)
            password_entry = tk.Entry(add_rtsp_window, show="*")  # show="*" to hide password
            port_entry = tk.Entry(add_rtsp_window)
            port_entry.insert(0, "554")  # Default port 554
            port_entry.grid(row=3, column=1, padx=10, pady=5)

            camera_name_entry.grid(row=0, column=1, padx=10, pady=5)
            ip_address_entry.grid(row=1, column=1, padx=10, pady=5)
            password_entry.grid(row=2, column=1, padx=10, pady=5)

            def save_info():
                camera_name = camera_name_entry.get()
                ip_address = ip_address_entry.get()
                password = password_entry.get()
                port = port_entry.get()


                rtsp = f"rtsp://admin:{password}@{ip_address}:{port}/H.265"
                name_rtsp= f"{camera_name}"
                add_rtsp(rtsp,name_rtsp)
                add_rtsp_window.destroy()
                choice_window.destroy()

            # Save button
            add_button = tk.Button(add_rtsp_window, text="Add RTSP", fg="white", bg="#444b54",
                                command=save_info)
            add_button.grid(row=4, column=0, columnspan=2, pady=10)
        def other_function():
            other_window = tk.Toplevel(choice_window)
            other_window.title("Enter RTSP Link and Name")
            other_window.resizable(False,False)
            other_window.configure(bg="#01a1ff",borderwidth=1, highlightthickness=2,highlightcolor="white")
            other_window.geometry(f"+{x+50}+{y}")
            # Labels and Entry fields for RTSP Link and Name
            tk.Label(other_window, text="RTSP Link:").grid(row=1, column=0, padx=10, pady=5)
            tk.Label(other_window, text="Name cam:").grid(row=0, column=0, padx=10, pady=5)
            rtsp_name_entry = tk.Entry(other_window)
            rtsp_link_entry = tk.Entry(other_window)
            
            rtsp_name_entry.grid(row=0, column=1, padx=10, pady=5)
            rtsp_link_entry.grid(row=1, column=1, padx=10, pady=5)
            

            def add_rtsp_link():
                rtsp_link = rtsp_link_entry.get()
                rtsp_name = rtsp_name_entry.get()
                if rtsp_link and rtsp_name:
                    add_rtsp(rtsp_link,rtsp_name)
                    other_window.destroy()
                    choice_window.destroy()
                else:
                    messagebox.showerror("lỗi", "Bạn chưa nhập đủ các thông tin")
                    other_window.lift()

            # Add button
            add_button = tk.Button(other_window, text="Add RTSP", fg="white", bg="#444b54", command=add_rtsp_link)
            add_button.grid(row=2, column=0, columnspan=2, pady=10)


        tk.Label(choice_window, text="Choose an option:").pack(pady=10)

        # Button to open window for entering camera information
        add_info_button = tk.Button(choice_window, text="Add Camera Info", command=add_rtsp_window)
        add_info_button.pack(pady=10)

        # Button for some other functionality
        other_button = tk.Button(choice_window, text="Add with link", command=other_function)
        other_button.pack(pady=10)


    def delete_rtsp(self):
        # Dummy function to delete selected RTSP entries
        selected_indices = []
        for idx, (var, chk_btn) in enumerate(self.rtsp_checkbuttons):
            if var.get():
                selected_indices.append(idx)
        # Remove selected RTSP entries from list and UI
        for idx in reversed(selected_indices):
            del self.rtsp_checkbuttons[idx]
            self.rtsp_list.pop(idx)
            self.name_cam_list.pop(idx)
        

        # Refresh the UI to reflect changes
        self.save_rtsp_list_to_file()
        self.show_rtsp()                
    def save_rtsp_list_to_file(self):
        file_path = "assets/rtsp/rtsp.txt"  # Directly specify the file name
        file_path_2="assets/rtsp/rtsp_name.txt"
        # Open the file in write mode with UTF-8 encoding
        if not os.path.exists(file_path):
            # If the file doesn't exist, create an empty file
            with open(file_path, 'w') as f:
                pass  # This will create an empty file
        if not os.path.exists(file_path_2):
            # If the file doesn't exist, create an empty file
            with open(file_path_2, 'w') as f:
                pass  # This will create an empty file

        with open(file_path, 'w', encoding='utf-8') as file:
            # Get all items from the Listbox and write them to the file
            for item in self.rtsp_list:
                file.write(f"{item}\n")
        with open(file_path_2, 'w', encoding='utf-8') as file:
            # Get all items from the Listbox and write them to the file
            for item in self.name_cam_list:
                file.write(f"{item}\n")

    def draw_line_function(self):
        self.define_var()
        if len(rtsp_selected) == 0:
            messagebox.showerror("lỗi","Bạn chưa chọn camera")
        elif len(rtsp_selected) > 0:
            # if self.options_check["count"]:
            for i,cam_info in enumerate(info_cams):
                if cam_info[f"cam_{i}"]["is_select"]:
                    self.lines_coor=[(coords, label) for (coords, label) in self.lines_coor if label != f'line_cam_{i}']
                    draw_window = Drawing_Line_Window(self, cam_info[f"cam_{i}"])  # Pass cam_info instead of info_cams[0]
                    lines.append(draw_window)
    def draw_polygon_function(self):
        self.define_var()
        if len(rtsp_selected) == 0:
            messagebox.showerror("lỗi","Bạn chưa chọn camera")
        elif len(rtsp_selected) > 0:
            # if self.options_check["count"]:
            for i,cam_info in enumerate(info_cams):
                if cam_info[f"cam_{i}"]["is_select"]:
                    self.polygon_coor=[(coords, label) for (coords, label) in self.polygon_coor if label != f'polygon_cam_{i}']
                    draw_window = Drawing_Polygon_Window(self, cam_info[f"cam_{i}"])  # Pass cam_info instead of info_cams[0]
                    polygon.append(draw_window)
            # lines.clear()


        


    def toggle_track(self):
        # print(option_function[0].get())
        i = 0
        if option_function[0].get():
            for var, chk_btn in self.option_checkbuttons:
                if i ==0 :
                    i+=1
                    continue
                # var.set(True)
                # option_function[i].set(True)
                chk_btn.config(state=tk.NORMAL)
                i+=1
        else:
            for var, chk_btn in self.option_checkbuttons:
                if i ==0 :
                    i+=1
                    continue
                var.set(False)
                option_function[i].set(False)
                chk_btn.config(state=tk.DISABLED)
                i+=1
            # for idx,option in enumerate(self.option_checkbuttons):
            #     for var, chk_btn in option:
            #         if idx > 0:
            #             chk_btn.config(state=tk.DISABLED)
            #             option_function[idx].set(False)
                        # var.set(False)

    def icon_resize(self,img):
        width,height=int(self.width/20),int(self.height/18)
        img_resized = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img_resized)
    def icon_resize_small(self,img):
        width,height=int(self.width/30),int(self.height/26)
        img_resized = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img_resized)
    
    def icon_fisrt(self, image_path):
        img = Image.open(image_path)
        img = img.convert("RGBA")
        return img
    def load_icons(self):
        icon_paths = {
            'home': "assets/frame0/Icon/Asset 34.png",
            'rtsp': "assets/frame0/Icon/Asset 36.png",
            'class': "assets/frame0/Icon/Asset 38.png",
            'function': "assets/frame0/Icon/Asset 40.png",
            'setting': "assets/frame0/Icon/Asset 42.png",
            'prev': "assets/frame0/Icon/Asset 45.png",
            'play': "assets/frame0/Icon/Asset 44.png",
            'stop': "assets/frame0/Icon/Asset 46.png",
            'next': "assets/frame0/Icon/Asset 47.png",
            'multicam': "assets/frame0/Icon/Asset 48.png",
            'file': "assets/frame0/Icon/Asset 43.png",
            'record': "assets/frame0/Icon/Asset 49.png",
            'select_all': "assets/frame0/Icon/Asset 51.png",
            'add': "assets/frame0/Icon/Asset 52.png",
            'delete': "assets/frame0/Icon/Asset 53.png"
        }

        
        for name, path in icon_paths.items():
            self.icons[name] = self.icon_fisrt(path)

    def update_background_image(self):
        resized_image = cv2.resize(self.image_item, (self.width, self.height))
        image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_item_rgb)
        self.background_photo = ImageTk.PhotoImage(image=image_pil)
        if hasattr(self, "background_label"):
            self.background_label.config(image=self.background_photo)
        else:
            # print("cc")
            self.background_label = tk.Label(self, image=self.background_photo)
            self.background_label.place(x=0, y=0)

    def open_website(self):
        webbrowser.open("https://asaai.id.vn/")
    def open_folder(self):
        folder_path = "save"  
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", folder_path])

    # def read_from_rtsp_file(self,file_path):
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         lines = file.readlines()
    #     # Initialize the lists
    #     a = []
    #     b = []

    #     # Process each line
    #     for line in lines:
    #         parts = line.strip().split()
    #         if len(parts) == 2:
    #             a.append(parts[0].strip('"'))
    #             b.append(parts[1].strip('"'))
    #     return a,b
    
    def read_from_file(self,file_path):
        if not os.path.exists(file_path):
            # If the file doesn't exist, create an empty file
            with open(file_path, 'w') as f:
                pass  # This will create an empty file
        with open(file_path, 'r') as file:
            classes = [line.strip() for line in file]
        return classes
    
    def update_size(self):

        for name,icon in self.icons.items():
            self.icons_resize[name]= self.icon_resize(icon)
        # #icon doc
        # self.back_button.config(image=self.icons_resize["home"])
        # self.rtsp_button.config(image=self.icons_resize["rtsp"])
        # self.class_button.config(image=self.icons_resize["class"])
        # self.function_button.config(image=self.icons_resize["function"])
        # self.setting_button.config(image=self.icons_resize["setting"])
        # #icon ngang
        # self.play_button.config(image=self.icons_resize["play"])
        # self.multicam_button.config(image=self.icons_resize["multicam"])
        # Update button images
        button_icons = {
            "home": self.back_button,
            "rtsp": self.rtsp_button,
            "class": self.class_button,
            "function": self.function_button,
            "setting": self.setting_button,
            "play": self.play_button,
            "stop": self.stop_button,
            "prev": self.prev_button,
            "next": self.next_button,
            "multicam": self.multicam_button,
            "file": self.file_button
        }

        for icon_name, button in button_icons.items():
            button.config(image=self.icons_resize[icon_name])
        

        self.back_button.place(x= (self.width)/18 ,y = self.height/6.8 )
        self.rtsp_button.place(x=(self.width)/18 , y=self.height / 3.5 )
        self.class_button.place(x=(self.width)/18 , y=self.height / 2.4 )
        self.function_button.place(x=(self.width)/18 , y=self.height * 0.56 )
        self.setting_button.place(x=(self.width)/18 , y=self.height * 0.7 )

        if self.is_running:
            self.play_button.place_forget()
            self.stop_button.place(x=(self.width)*0.53,y=self.height * 0.88)
        else :
            self.stop_button.place_forget() 
            self.play_button.place(x=(self.width)*0.53,y=self.height * 0.88)
        self.prev_button.place(x=(self.width)*0.453,y=self.height * 0.88)
        self.next_button.place(x=(self.width)*0.6,y=self.height * 0.88)
        self.multicam_button.place(x=(self.width)*0.8,y=self.height * 0.88)
        self.file_button.place(x=(self.width)/18,y=self.height * 0.88)

        if not self.ismulticam:
            resized_image = cv2.resize(self.frame_item, (int(self.width*0.748), int(self.height*0.7)))
            image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_item_rgb)
            self.frame_photo = ImageTk.PhotoImage(image=image_pil)
            self.frame_label.config(image=self.frame_photo)
            self.frame_label.place_configure(x=(self.width)*0.555, y=self.height*0.468,anchor="center")

        else:
            resized_image = cv2.resize(self.frame_item, (int(self.width * (0.748 / 2)), int(self.height * (0.7 / 2))))
            image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_item_rgb)
            self.frame_photo = ImageTk.PhotoImage(image=image_pil)

            frame_positions = [
                (self.width * 0.36, self.height * 0.28),
                (self.width * 0.75, self.height * 0.28),
                (self.width * 0.36, self.height * 0.645),
                (self.width * 0.75, self.height * 0.645)
            ]

            for i, (label, (x, y)) in enumerate(zip(
                    [self.frame_label_1, self.frame_label_2, self.frame_label_3, self.frame_label_4],
                    frame_positions)):
                label.config(image=self.frame_photo)
                label.place_configure(x=x, y=y, anchor="center")

    def on_resize(self, event):
        self.width = max(self.winfo_width(), MIN_CANVAS_WIDTH)
        # print(self.width)
        self.height = max(self.winfo_height(), MIN_CANVAS_HEIGHT)
        self.update_background_image()
        self.update_size()


class Drawing_Line_Window(tk.Toplevel):
    def __init__(self, parent, cam_info):
        super().__init__(parent)
        self.parent = parent
        self.cam_info = cam_info
        self.lines = []
        self.setup_ui()

    def setup_ui(self):
        self.open_draw_window(self.cam_info['line_name'], self.cam_info['rtsp'])

    def open_draw_window(self, cam_line, rtsp):
        if rtsp == "0":
            rtsp=0
        cap = cv2.VideoCapture(rtsp)
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("lỗi", f"Không xem được cam {rtsp}.")
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame[::3, ::3]
        self.frame_height, self.frame_width = frame.shape[:2]
        self.original_frame = frame
        self.frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

        self.canvas = tk.Canvas(self, width=self.frame_width, height=self.frame_height + 20)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_image)

        self.canvas.bind("<ButtonPress-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", lambda event, cam_line=cam_line: self.end_line(event, cam_line))

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_lines)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.undo_button = tk.Button(self, text="Undo", command=self.undo_line)
        self.undo_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_line_button = tk.Button(self, text="Save", command=self.save_line)
        self.save_line_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.start_label = tk.Label(self, text="Start: (0, 0)")
        self.start_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.end_label = tk.Label(self, text="End: (0, 0)")
        self.end_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.line_drawing = []
        self.lines_notsave = self.lines
        self.drawing_enabled = True
        self.start_x = self.start_y = self.end_x = self.end_y = 0

    def start_line(self, event):
        if self.drawing_enabled:
            self.start_x, self.start_y = event.x, event.y
            self.start_label.config(text=f"Start: ({self.start_x}, {self.start_y})")
            self.current_line = None

    def draw_line(self, event):
        if self.drawing_enabled and self.current_line:
            self.canvas.delete(self.current_line)
        self.end_x, self.end_y = event.x, event.y
        self.end_label.config(text=f"End: ({self.end_x}, {self.end_y})")
        self.current_line = self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y)

    def end_line(self, event, cam_line):
        if self.drawing_enabled:
            line = {(self.start_x, self.start_y), (self.end_x, self.end_y)}
            self.lines_notsave.append((line, f"{cam_line}"))
            self.line_drawing.append(self.current_line)
            self.current_line = None

    def clear_lines(self):
        for line in self.line_drawing:
            self.canvas.delete(line)
        self.line_drawing = []
        self.lines_notsave = []
        self.start_label.config(text="Start: (0, 0)")
        self.end_label.config(text="End: (0, 0)")

    def save_line(self):
        self.lines = self.lines_notsave

    def undo_line(self):
        if self.line_drawing:
            last_line = self.line_drawing.pop()
            self.lines_notsave.pop()
            self.canvas.delete(last_line)
        self.start_label.config(text="Start: (0, 0)")
        self.end_label.config(text="End: (0, 0)")
class Drawing_Polygon_Window(tk.Toplevel):
    def __init__(self, parent, cam_info):
        super().__init__(parent)
        self.parent = parent
        self.cam_info = cam_info
        self.polygons = []
        self.setup_ui()

    def setup_ui(self):
        self.open_draw_window(self.cam_info['polygon_name'], self.cam_info['rtsp'])

    def open_draw_window(self, cam_polygon, rtsp):
        if rtsp == "0":
            rtsp = 0
        cap = cv2.VideoCapture(rtsp)
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("lỗi", f"Không xem được cam {rtsp}.")
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame[::3, ::3]
        self.frame_height, self.frame_width = frame.shape[:2]
        self.original_frame = frame
        self.frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

        self.canvas = tk.Canvas(self, width=self.frame_width, height=self.frame_height + 20)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_image)

        self.canvas.bind("<ButtonPress-1>", self.start_polygon)
        self.canvas.bind("<B1-Motion>", self.draw_polygon)
        self.canvas.bind("<ButtonRelease-1>", lambda event, cam_polygon=cam_polygon: self.end_polygon(event, cam_polygon))

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_polygons)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.undo_button = tk.Button(self, text="Undo", command=self.undo_polygon)
        self.undo_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_polygon_button = tk.Button(self, text="Save", command=self.save_polygon)
        self.save_polygon_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.start_label = tk.Label(self, text="Start: (0, 0)")
        self.start_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.end_label = tk.Label(self, text="End: (0, 0)")
        self.end_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.current_polygon_points = []
        self.polygon_drawing = []
        self.polygons_notsave = self.polygons
        self.drawing_enabled = True
        self.current_polygon = None

    def start_polygon(self, event):
        if self.drawing_enabled:
            self.current_polygon_points.append((event.x, event.y))
            self.start_label.config(text=f"Start: ({event.x}, {event.y})")

    def draw_polygon(self, event):
        if self.drawing_enabled:
            if self.current_polygon:
                self.canvas.delete(self.current_polygon)
            self.current_polygon_points.append((event.x, event.y))
            self.end_label.config(text=f"End: ({event.x}, {event.y})")
            self.current_polygon = self.canvas.create_polygon(self.current_polygon_points, outline='red', fill='', width=2)

    def end_polygon(self, event,cam_polygon):
        if self.drawing_enabled:
            self.current_polygon_points.append((event.x, event.y))
            self.polygons_notsave.append((self.current_polygon_points, f"{cam_polygon}"))
            self.polygon_drawing.append(self.current_polygon)
            self.current_polygon = None
            self.current_polygon_points = []

    def clear_polygons(self):
        for polygon in self.polygon_drawing:
            self.canvas.delete(polygon)
        self.polygon_drawing = []
        self.polygons_notsave = []
        self.start_label.config(text="Start: (0, 0)")
        self.end_label.config(text="End: (0, 0)")

    def save_polygon(self):
        self.polygons = self.polygons_notsave
        # print(self.polygons)

    def undo_polygon(self):
        if self.polygon_drawing:
            last_polygon = self.polygon_drawing.pop()
            self.polygons_notsave.pop()
            self.canvas.delete(last_polygon)
        self.start_label.config(text="Start: (0, 0)")
        self.end_label.config(text="End: (0, 0)")
    
def main():
    # root=tk.Tk()
    app = StartPage()
    app.iconphoto(True, tk.PhotoImage(file="assets/frame0/logo.png"))
    app.mainloop()



if __name__ == "__main__":
    main()
