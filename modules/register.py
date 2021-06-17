from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd

def logi(root):
    try:
        r2.destroy()
        r3.destroy()
    except:
        pass
    l.log(root)


def mai(root):
    try:
        r2.destroy()
    except:
        pass
    global r1
    r1 = Frame(root, height=700, width=1050)
    r1.place(x=0, y=0)
    r1.render = PhotoImage(file="elements/Registration_bg.png")
    img = Label(r1, image=r1.render)
    img.place(x=0, y=0)
    r1.Img1 = PhotoImage(file="elements/recruiter_element.png")
    recruit = Button(r1, image=r1.Img1, border=0, bg="#03DDEE",
                     relief="raised", activebackground="#03EAFD", command=lambda: recruiter_regis(root))
    recruit.place(x=140, y=340)
    r1.Img2 = PhotoImage(file="elements/client_element.png")
    recruit2 = Button(r1, image=r1.Img2, border=0, bg="#05edFC",
                      relief="raised", activebackground="#05F6FD", command=lambda: client_regis(root))
    recruit2.place(x=360, y=340)
    r1.bn = PhotoImage(file="elements\\backlogin.png")
    btn = Button(r1, image=r1.bn, bg='#05e4f6',
                 bd=0, activebackground="#05e4f6", command=lambda: logi(root))
    btn.place(x=220, y=550)


def recruiter_regis(root):
    global name, email, pwd, cpwd
    print("hello recruiter")
    r1.destroy()
    r2 = Frame(root, height=700, width=1050)
    r2.place(x=0, y=0)
    r2.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r2, image=r2.render)
    img.place(x=0, y=0)
    name_l = Label(r2, text="Name : ", bg='#FFFFFF', fg="#00B9ED",
                   font=('normal', 20, 'bold'))
    name_l.place(x=100, y=250)
    name = Entry(r2, placeholder='Enter Your Full Name...', width=20)
    name.place(x=290, y=250)

    email_l = Label(r2, text="Email : ", bg='#FFFFFF', fg="#00B9ED",
                    font=('normal', 20, 'bold'))
    email_l.place(x=100, y=300)
    email = Entry(r2, placeholder='Email', width=20)
    email.place(x=290, y=300)

    pwd_l = Label(r2, text="Password : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    pwd_l.place(x=100, y=350)
    pwd = Entry(r2, placeholder='Password', show="*", width=20)
    pwd.place(x=290, y=350)

    con_pwd_l = Label(r2, text="Confirm : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    con_pwd_l.place(x=100, y=400)
    cpwd = Entry(r2, placeholder='Confirm Password', show="*", width=20)
    cpwd.place(x=290, y=400)

    r2.bn = PhotoImage(file="elements\\next1.png")
    btn = Button(r2, image=r2.bn, bg='#FFFFFF', bd=0,
                 activebackground="#ffffff", command=lambda: recruiter_check(root))
    btn.place(x=320, y=500)

    r2.back = PhotoImage(file="elements\\back.png")
    btn2 = Button(r2, image=r2.back, bg='#FFFFFF', bd=0,
                  activebackground="#ffffff", command=lambda: mai(root))
    btn2.place(x=120, y=500)


def recruiter_check(root):
    global name1, email1, pwd1, cpwd1
    name1 = name.get()
    email1 = email.get()
    pwd1 = pwd.get()
    cpwd1 = cpwd.get()
    print(name1, email1, pwd1, cpwd1)
    if name1 and email1 and pwd1 and cpwd1:
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute('select email from users')
        total = cur.fetchall()
        mycon.close()
        exist_email = []
        for i in total:
            exist_email.append(i[0])
        print("existing users:", exist_email)

        if email1 in exist_email:
            messagebox.showinfo('ALERT!', 'EMAIL ALREADY REGISTERED')
            email.delete(0, END)

        else:
            if pwd1 == cpwd1:
                recruit_complete(root)
            else:
                messagebox.showinfo('ALERT!', 'PASSWORDS DO NOT MATCH')

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')


def recruit_complete(root):
    print("hello ", name1, ", Let's complete your profile")
    r3 = Frame(root, height=700, width=1050)
    r3.place(x=0, y=0)
    r3.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r3, image=r3.render)
    img.place(x=0, y=0)

    global gender, company, loc
    gender = StringVar()

    style = ttk.Style(r3)
    style.configure("TRadiobutton", background="white",
                    foreground="#696969", font=("arial", 16, "bold"))

    gender_l = Label(r3, text="Gender : ", bg='#FFFFFF', fg="#00B9ED",
                     font=('normal', 20, 'bold'))
    gender_l.place(x=100, y=250)
    ttk.Radiobutton(r3, text="Male", value="M", variable=gender).place(
        x=300, y=250)
    ttk.Radiobutton(r3, text="Female", value="F", variable=gender).place(
        x=400, y=250)

    company_l = Label(r3, text="Company : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    company_l.place(x=100, y=300)
    company = Entry(r3, placeholder='Company', width=20)
    company.place(x=290, y=300)

    loc_l = Label(r3, text="Location : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    loc_l.place(x=100, y=350)
    loc = Entry(r3, placeholder='Location', width=20)
    loc.place(x=290, y=350)

    r3.bn = PhotoImage(file="elements\\reg.png")
    btn = Button(r3, image=r3.bn, bg='#FFFFFF', bd=0,
                 activebackground="#ffffff", command=lambda: recruiter_submit(root))
    btn.place(x=320, y=500)


def recruiter_submit(root):
    global gender1, company1, loc1
    gender1 = gender.get()
    company1 = company.get()
    loc1 = loc.get()
    print(name1, email1, gender1, company1, loc1)
    if gender1 and company1 and loc1:
        exe = f'insert into users values("{name1}","{email1}","recruiter","{pwd1}")'
        exe1 = f'INSERT INTO mydb.Recruiter(RID, RName, REmail, CompanyName, CompanyLocation ,RGender) VALUES (NULL,"{name1}","{email1}","{company1}","{loc1}","{gender1}")'
        try:
            mycon = sql.connect(host='localhost', user='root',
                                passwd=user_pwd, database='mydb')
            cur = mycon.cursor()
            cur.execute(exe)
            cur.execute(exe1)
            name.delete(0, END)
            email.delete(0, END)
            pwd.delete(0, END)
            cpwd.delete(0, END)
            # gender.delete(0, END)
            loc.delete(0, END)
            company.delete(0, END)
            mycon.commit()
            mycon.close()
            messagebox.showinfo('SUCCESS!', 'Registration Successful')
            logi(root)
        except:
            pass

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')


def client_regis(root):
    global name, email, pwd, cpwd
    print("hello client")
    r1.destroy()
    r2 = Frame(root, height=700, width=1050)
    r2.place(x=0, y=0)
    r2.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r2, image=r2.render)
    img.place(x=0, y=0)

    name_l = Label(r2, text="Name : ", bg='#FFFFFF', fg="#00B9ED",
                   font=('normal', 20, 'bold'))
    name_l.place(x=100, y=250)
    name = Entry(r2, placeholder='Enter Your Full Name...', width=20)
    name.place(x=290, y=250)

    email_l = Label(r2, text="Email : ", bg='#FFFFFF', fg="#00B9ED",
                    font=('normal', 20, 'bold'))
    email_l.place(x=100, y=300)
    email = Entry(r2, placeholder='Email', width=20)
    email.place(x=290, y=300)

    pwd_l = Label(r2, text="Password : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    pwd_l.place(x=100, y=350)
    pwd = Entry(r2, placeholder='Password', show="*", width=20)
    pwd.place(x=290, y=350)

    con_pwd_l = Label(r2, text="Confirm : ", bg='#FFFFFF', fg="#00B9ED",
                      font=('normal', 20, 'bold'))
    con_pwd_l.place(x=100, y=400)
    cpwd = Entry(r2, placeholder='Confirm Password', show="*", width=20)
    cpwd.place(x=290, y=400)

    r2.bn = PhotoImage(file="elements\\next1.png")
    btn = Button(r2, image=r2.bn, bg='#FFFFFF', bd=0,
                 activebackground="#ffffff", command=lambda: client_check(root))
    btn.place(x=320, y=500)

    r2.back = PhotoImage(file="elements\\back.png")
    btn2 = Button(r2, image=r2.back, bg='#FFFFFF', bd=0,
                  activebackground="#ffffff", command=lambda: mai(root))
    btn2.place(x=120, y=500)


def client_check(root):
    global name1, email1, pwd1, cpwd1
    name1 = name.get()
    email1 = email.get()
    pwd1 = pwd.get()
    cpwd1 = cpwd.get()
    print(name1, email1, pwd1, cpwd1)
    if name1 and email1 and pwd1 and cpwd1:
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute('select email from users')
        total = cur.fetchall()
        mycon.close()
        exist_email = []
        for i in total:
            exist_email.append(i[0])
        print("existing users:", exist_email)

        if email1 in exist_email:
            messagebox.showinfo('ALERT!', 'EMAIL ALREADY REGISTERED')
            email.delete(0, END)

        else:
            if pwd1 == cpwd1:
                client_complete(root)
            else:
                messagebox.showinfo('ALERT!', 'PASSWORDS DO NOT MATCH')

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')


def client_complete(root):
    print("hello ", name1, ", Let's complete your profile")
    r3 = Frame(root, height=700, width=1050)
    r3.place(x=0, y=0)
    r3.render = PhotoImage(file="elements/reg_bg.png")
    img = Label(r3, image=r3.render)
    img.place(x=0, y=0)

    global gender, age, loc, workxp, qualification, skills
    gender = StringVar()

    style = ttk.Style(r3)
    style.configure("TRadiobutton", background="white",
                    foreground="#696969", font=("arial", 16, "bold"))

    gender_l = Label(r3, text="Gender : ", bg='#FFFFFF', fg="#00B9ED",
                     font=('normal', 20, 'bold'))
    gender_l.place(x=100, y=200)
    ttk.Radiobutton(r3, text="Male", value="M", variable=gender).place(
        x=300, y=200)
    ttk.Radiobutton(r3, text="Female", value="F", variable=gender).place(
        x=400, y=200)

    age_l = Label(r3, text="Age : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    age_l.place(x=100, y=250)
    age = Entry(r3, placeholder='Age', width=20)
    age.place(x=290, y=250)

    loc_l = Label(r3, text="Location : ", bg='#FFFFFF', fg="#00B9ED",
                  font=('normal', 20, 'bold'))
    loc_l.place(x=100, y=300)
    loc = Entry(r3, placeholder='Location', width=20)
    loc.place(x=290, y=300)

    workxp_l = Label(r3, text="Experience : ", bg='#FFFFFF', fg="#00B9ED",
                     font=('normal', 20, 'bold'))
    workxp_l.place(x=100, y=350)
    workxp = Entry(r3, placeholder='Work Experience(yrs)', width=20)
    workxp.place(x=290, y=350)

    qualification_l = Label(r3, text="Qualification : ",
                            bg='#FFFFFF', fg="#00B9ED", font=('normal', 20, 'bold'))
    qualification_l.place(x=100, y=400)
    qualification = Entry(r3, placeholder='Btech/BE...', width=20)
    qualification.place(x=290, y=400)

    skills_l = Label(r3, text="Skills : ", bg='#FFFFFF',
                     fg="#00B9ED", font=('normal', 20, 'bold'))
    skills_l.place(x=100, y=450)
    skills = Entry(r3, placeholder='separated by comma', width=20)
    skills.place(x=290, y=450)

    r3.bn = PhotoImage(file="elements\\reg.png")
    btn = Button(r3, image=r3.bn, bg='#FFFFFF', bd=0,
                 activebackground="#ffffff", command=lambda: client_submit(root))
    btn.place(x=320, y=550)


def client_submit(root):
    global gender1, age1, loc1, workxp1, qualification1, skills1
    gender1 = gender.get()
    age1 = age.get()
    loc1 = loc.get()
    workxp1 = workxp.get()
    qualification1 = qualification.get()
    skills1 = skills.get()
    print(name1, email1, gender1, age1, loc1, workxp1, qualification1, skills1)
    if gender1 and age1 and loc1 and workxp1:
        exe = f'insert into users values("{name1}","{email1}","client","{pwd1}")'
        exe1 = f'INSERT INTO mydb.Client(CID, CName , CEmail, CAge, CLocation, CGender, CExp, CSkills, CQualification ) VALUES (NULL, "{name1}", "{email1}", {age1}, "{loc1}", "{gender1}", {workxp1}, "{skills1}", "{qualification1}");'
        try:
            mycon = sql.connect(host='localhost', user='root',
                                passwd=user_pwd, database='mydb')
            cur = mycon.cursor()
            cur.execute(exe)
            cur.execute(exe1)
            name.delete(0, END)
            email.delete(0, END)
            pwd.delete(0, END)
            cpwd.delete(0, END)
            # gender.delete(0, END)
            loc.delete(0, END)
            age.delete(0, END)
            workxp.delete(0, END)
            qualification.delete(0, END)
            skills.delete(0, END)
            mycon.commit()
            mycon.close()
            messagebox.showinfo('SUCCESS!', 'Registration Successful')
            logi(root)
        except:
            pass

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS ARE MUST BE FILLED')
