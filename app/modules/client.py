from tkinter import (
    Button,
    Frame,
    Label,
    PhotoImage,
    Scrollbar,
    messagebox,
    ttk,
)

import modules.login as login_mod
from utils.database import db_connection
from utils.variables import ELEMENTS_FOLDER


def get_details(email):
    global name, location, gen, clicid
    q = (
        "select CName,CLocation,CGender,CID "
        + f'from hireme.client where CEmail="{email}"'
    )

    with db_connection.managed_cursor() as cur:
        cur.execute(q)
        d = cur.fetchall()

    name = d[0][0]
    location = d[0][1]
    gen = d[0][2]
    clicid = d[0][3]


def logi(root):
    try:
        bg.destroy()
    except Exception as e:
        print(e)
    login_mod.log(root)


def apply(table):
    # fetch cid,jid from treeview that is in available jobs function
    # code
    selectedindex = table.focus()  # that will return number index
    # that will return list of values with columns=['JID','JobRole',
    # 'JobType', 'CompanyName', 'CompanyLocation',
    # 'Qualification','MinExp', 'Salary']
    selectedvalues = table.item(selectedindex, "values")
    ajid = selectedvalues[0]
    chkquery = (
        f"SELECT * from hireme.application where cid={clicid} and jid={ajid}"
    )

    with db_connection.managed_cursor() as cur:
        cur.execute(chkquery)
        tempbuff = cur.fetchall()

    if tempbuff:
        messagebox.showinfo(
            "Oops", "It seems like you have already applied to this job"
        )
    else:
        query = (
            "Insert into application values (NULL,(select rid from hireme.job "
            + f"where job.jid={ajid}),{ajid},{clicid})"
        )
        queryapplyjob = query

        with db_connection.managed_cursor() as cur:
            cur.execute(queryapplyjob)

        messagebox.showinfo("Thanks", "Your application has been submitted")


def delet(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, "values")
    aaid = selectedvalues[0]

    with db_connection.managed_cursor() as cur:
        cur.execute(f"delete from hireme.application where aid={aaid}")

    messagebox.showinfo("Thanks", "Your application has been Deleted")
    myapp()


def sort_alljobs(table):
    criteria = search_d.get()
    if not criteria == "Select":
        table.delete(*table.get_children())

        with db_connection.managed_cursor() as cur:
            query = (
                "select job.JID,job.JobRole,job.JobType, recruiter.CompanyName"
                + ", recruiter.CompanyLocation, job.Qualification, job.MinExp,"
                + " job.Salary from hireme.job JOIN hireme.recruiter ON "
                + f"job.rid=recruiter.rid order by {criteria}"
            )
            cur.execute(query)
            jobs = cur.fetchall()

        i = 0
        for r in jobs:
            table.insert(
                "",
                i,
                text="",
                values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]),
            )
            i += 1


def sort_myapplications(table):
    criteria = search_d.get()
    if not criteria == "Select":
        table.delete(*table.get_children())

        with db_connection.managed_cursor() as cur:
            query = (
                "SELECT application.aid,job.JobRole, job.JobType,"
                + "recruiter.CompanyName, recruiter.CompanyLocation, "
                + "job.qualification, job.minexp, job.salary FROM application "
                + "JOIN recruiter ON application.rid=recruiter.rid JOIN job ON"
                + " application.jid=job.jid where "
                + f"application.CID={clicid} order by {criteria}"
            )
            cur.execute(query)
            jobs = cur.fetchall()

        i = 0
        for r in jobs:
            table.insert(
                "",
                i,
                text="",
                values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]),
            )
            i += 1


def showalljobs(table):
    with db_connection.managed_cursor() as cur:
        query = (
            "select job.JID,job.JobRole,job.JobType, recruiter.CompanyName,"
            + "recruiter.CompanyLocation, job.Qualification, job.MinExp, "
            + "job.Salary from hireme.job JOIN hireme.recruiter ON "
            + "job.rid=recruiter.rid"
        )
        cur.execute(query)
        jobs = cur.fetchall()
    i = 0
    for r in jobs:
        table.insert(
            "",
            i,
            text="",
            values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]),
        )
        i += 1


def show_myapplications(table):
    with db_connection.managed_cursor() as cur:
        query = (
            "SELECT application.aid,job.JobRole, job.JobType,"
            + "recruiter.CompanyName, recruiter.CompanyLocation,"
            + "job.qualification, job.minexp, job.salary FROM "
            + "application JOIN recruiter ON application.rid=recruiter.rid "
            + "JOIN job ON application.jid=job.jid where "
            + f"application.CID={clicid}"
        )
        cur.execute(query)
        applications = cur.fetchall()

    print(applications)
    i = 0
    for x in applications:
        table.insert(
            "",
            i,
            text="",
            values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]),
        )
        i += 1


def available():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=("normal", 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(
        rt, width=12, font=("normal", 18), state="readonly"
    )
    search_d["values"] = ("Select", "JobRole", "JobType", "CompanyLocation")
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(
        rt,
        text="Sort",
        font=("normal", 12, "bold"),
        bg="#00b9ed",
        fg="#ffffff",
        command=lambda: sort_alljobs(table),
    )
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    apl = Button(
        rt,
        text="Apply",
        font=("normal", 12, "bold"),
        bg="#00b9ed",
        fg="#ffffff",
        command=lambda: apply(table),
    )
    apl.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(
        tab,
        columns=(
            "JID",
            "JobRole",
            "JobType",
            "CompanyName",
            "CompanyLocation",
            "Qualification",
            "MinExp",
            "Salary",
        ),
        xscrollcommand=scx.set,
        yscrollcommand=scy.set,
    )
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JID")
    table.heading("JobRole", text="JobRole")
    table.heading("JobType", text="JobType")
    table.heading("CompanyName", text="CompanyName")
    table.heading("CompanyLocation", text="CompanyLocation")
    table.heading("Qualification", text="Qualification")
    table.heading("MinExp", text="MinExp")
    table.heading("Salary", text="Salary")

    table["show"] = "headings"

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=100)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("CompanyName", width=150)
    table.column("CompanyLocation", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=100)
    table.column("Salary", width=150)
    showalljobs(table)
    table.pack(fill="both", expand=1)


def myapp():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=("normal", 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(
        rt, width=12, font=("normal", 18), state="readonly"
    )
    search_d["values"] = ("Select", "JobRole", "JobType", "CompanyLocation")
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(
        rt,
        text="Sort",
        font=("normal", 12, "bold"),
        bg="#00b9ed",
        fg="#ffffff",
        command=lambda: sort_myapplications(table),
    )
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    dlt = Button(
        rt,
        text="Delete",
        font=("normal", 12, "bold"),
        bg="#00b9ed",
        fg="#ffffff",
        command=lambda: delet(table),
    )
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(
        tab,
        columns=(
            "AID",
            "JobRole",
            "JobType",
            "CompanyName",
            "CompanyLocation",
            "Qualification",
            "MinExp",
            "Salary",
        ),
        xscrollcommand=scx.set,
        yscrollcommand=scy.set,
    )
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("AID", text="AID")
    table.heading("JobRole", text="JobRole")
    table.heading("JobType", text="JobType")
    table.heading("CompanyName", text="CompanyName")
    table.heading("CompanyLocation", text="CompanyLocation")
    table.heading("Qualification", text="Qualification")
    table.heading("MinExp", text="MinExp")
    table.heading("Salary", text="Salary")
    table["show"] = "headings"

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("AID", width=50)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)


def cli(root, email1):
    global email
    email = email1
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    get_details(email)

    bg.load = PhotoImage(file=str(ELEMENTS_FOLDER / "bg{gen}.png"))
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    # Navbar
    nm = Label(
        root,
        text=f"{name}",
        font=("normal", 36, "bold"),
        bg="#ffffff",
        fg="#0A3D62",
    )
    nm.place(x=300, y=50)
    cp = Label(
        root,
        text=f"{location}",
        font=("normal", 24),
        bg="#ffffff",
        fg="#0A3D62",
    )
    cp.place(x=300, y=120)
    bn = Button(
        root,
        text="LOGOUT",
        font=("normal", 20),
        bg="#b32e2e",
        fg="#ffffff",
        command=lambda: logi(root),
    )
    bn.place(x=800, y=75)

    # Left
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=240)
    pj = Button(
        lf,
        text="Available Jobs",
        font=("normal", 20),
        bg="#b32e2e",
        fg="#ffffff",
        command=available,
    )
    pj.grid(row=0, column=0, padx=60, pady=70)
    ap = Button(
        lf,
        text="My Applications",
        font=("normal", 20),
        bg="#b32e2e",
        fg="#ffffff",
        command=myapp,
    )
    ap.grid(row=1, column=0, padx=60, pady=70)

    # Right
    global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file=str(ELEMENTS_FOLDER / "bgr.png"))
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)
