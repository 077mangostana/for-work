import customtkinter as ctk
from tkinter import messagebox
import json
import os
import random
from datetime import datetime, date

def normalize_date(text):
    text = text.strip()
    if len(text) == 6 and text.isdigit():
        yy = text[0:2]
        mm = text[2:4]
        dd = text[4:6]
        return "20" + yy + "-" + mm + "-" + dd
    return text

DATA_FILE = "commissions.json"


CHEERS = [
    "Yay! Another one done! You're amazing!",
    "Perfect delivery! The commission is in love!",
    "One less work-in-progress! Great job!",
    "You crushed it! Who is next?",
    "Your magical paintbrush saves the day again!",
    "Time to reward yourself with a treat!",
]


PEP_TALKS = [
    "You are doing great. Keep going!",
    "Slow progress is still progress. Breathe.",
    "Remember to drink water and stretch!",
    "One stroke at a time. You've got this!",
    "Snack break? Snack break.",
    "Why did past-you accept this deadline? Love you though.",
    "You are a magician. Do not forget that.",
    "Bad sketch days happen. Tomorrow will be better.",
]


#data
def load_data():
    if os.path.exists(DATA_FILE):
        f = open(DATA_FILE, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data
    return []

#save
def save_data(data):
    f = open(DATA_FILE, "w", encoding="utf-8")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.close()

#count
def count_done(data):
    count = 0
    for c in data:
        if c[6] == "Done":
            count = count + 1
    return count

#doing process
def count_doing(data):
    count = 0
    for c in data:
        if c[6] != "Done":
            count = count + 1
    return count

#income
def total_income(data):
    total = 0
    for c in data:
        if c[6] == "Done":
            try:
                total = total + float(c[2])
            except:
                pass
    return total


def get_title(done_count):
    if done_count >= 250:
        return "Legendary Artist"
    if done_count >= 160:
        return "Art Royalty"
    if done_count >= 100:
        return "Star Artist"
    if done_count >= 50:
        return "Skilled Artist"
    if done_count >= 20:
        return "Sprout Artist"
    return "Baby Artist"


#main window
window = ctk.CTk()
window.title("Cozy Studio")
window.geometry("700x600")


#t=status bar
status_label = ctk.CTkLabel(window, text="", justify="left")
status_label.pack(pady=10)


def refresh_status():
    #refresh
    data = load_data()
    done = count_done(data)
    doing = count_doing(data)
    money = total_income(data)
    title = get_title(done)
    text = "Title: " + title + "    Done: " + str(done) + "    In progress: " + str(doing) + "    Total earned: $" + str(money)
    status_label.configure(text=text)


#content box
content_box = ctk.CTkTextbox(window, width=650, height=350)
content_box.pack(pady=10)


def set_content(text):
    content_box.delete("1.0", "end")
    content_box.insert("1.0", text)


#main functions

def show_schedule():
    data = load_data()
    todo = []
    for c in data:
        if c[6] != "Done":
            todo.append(c)

    if len(todo) == 0:
        set_content("No active commissions. Time to relax!")
        return

    #date 
    n = len(todo)
    for i in range(n):
        for j in range(n - 1 - i):
            if todo[j][3] > todo[j + 1][3]:
                temp = todo[j]
                todo[j] = todo[j + 1]
                todo[j + 1] = temp

    today = date.today()
    text = "⭐⭐⭐Schedule (by start date)⭐⭐⭐\n\n"
    for c in todo:
        mark = ""
        try:
            start = datetime.strptime(c[3], "%Y-%m-%d").date()
            if start == today:
                mark = "  (starts today!)"
            elif start < today:
                mark = "  (in progress)"
            else:
                days = (start - today).days
                mark = "  (starts in " + str(days) + " day(s))"
        except:
            mark = "  (invalid date)"

        text = text + c[0] + " | " + c[1] + mark + "\n"
        text = text + "   Start: " + c[3] + "   Deadline: " + c[4] + "\n"
        text = text + "   Price: " + c[2] + "\n\n"

    set_content(text)


def show_pep_talk():
    set_content(random.choice(PEP_TALKS))


def open_add_window():
    #popup windows
    popup = ctk.CTkToplevel(window)
    popup.title("New commission")
    popup.geometry("400x500")
    popup.after(100, popup.lift)
    popup.after(100, popup.grab_set)

    #input name
    ctk.CTkLabel(popup, text="Commissioner name").pack(pady=2)
    entry_commission = ctk.CTkEntry(popup, width=300)
    entry_commission.pack()

    #input type
    ctk.CTkLabel(popup, text="Commission type(private/commercial)").pack(pady=2)
    entry_type = ctk.CTkEntry(popup, width=300)
    entry_type.pack()

    #input price
    ctk.CTkLabel(popup, text="Price (numbers only)").pack(pady=2)
    entry_price = ctk.CTkEntry(popup, width=300)
    entry_price.pack()

    #input startdate
    ctk.CTkLabel(popup, text="Start date (YYMMDD)").pack(pady=2)
    entry_start = ctk.CTkEntry(popup, width=300)
    entry_start.pack()

    #input deadline
    ctk.CTkLabel(popup, text="Deadline (YYMMDD)").pack(pady=2)
    entry_deadline = ctk.CTkEntry(popup, width=300)
    entry_deadline.pack()

    #input requests
    ctk.CTkLabel(popup, text="commission's requests").pack(pady=2)
    entry_requests = ctk.CTkEntry(popup, width=300)
    entry_requests.pack()

    def save():
        commissioner = entry_commission.get()
        if commissioner.strip() == "":
            messagebox.showwarning("Oops", "Please enter the commissioner name.")
            return
        data = load_data()
        data.append([
            commissioner,
            entry_type.get(),
            entry_price.get(),
            normalize_date(entry_start.get()),
            normalize_date(entry_deadline.get()),
            entry_requests.get(),
            "In progress",
        ])
        save_data(data)
        popup.destroy()
        refresh_status()
        show_schedule()

    ctk.CTkButton(popup, text="Save", command=save).pack(pady=10)


def open_search_window():
    popup = ctk.CTkToplevel(window)
    popup.title("Search")
    popup.geometry("400x150")
    popup.after(100, popup.lift)
    popup.after(100, popup.grab_set)

    ctk.CTkLabel(popup, text="Commissioner name(partial okay)").pack(pady=5)
    entry_name = ctk.CTkEntry(popup, width=300)
    entry_name.pack()

    def do_search():
        name = entry_name.get()
        data = load_data()
        text = ""
        found = False
        for c in data:
            if name.lower() in c[0].lower():
                text = text + c[0] + " | " + c[1] + "\n"
                text = text + "   Price: " + c[2] + "    Status: " + c[6] + "\n"
                text = text + "   Start: " + c[3] + "   Deadline: " + c[4] + "\n"
                text = text + "   Requests: " + c[5] + "\n\n"
                found = True
        if found == False:
            text = "No matching commissions found."
        set_content(text)
        popup.destroy()

    ctk.CTkButton(popup, text="Search", command=do_search).pack(pady=10)


def open_finish_window():
    data = load_data()
    todo = []
    for i in range(len(data)):
        if data[i][6] != "Done":
            todo.append([i, data[i][0], data[i][1]])

    if len(todo) == 0:
        set_content("Nothing to finish! You're all caught up.")
        return

    popup = ctk.CTkToplevel(window)
    popup.title("Finish a commission")
    popup.geometry("400x400")
    popup.after(100, popup.lift)
    popup.after(100, popup.grab_set)

    ctk.CTkLabel(popup, text="Click one to mark as done:").pack(pady=5)

    def make_finish(idx):
        def do_finish():
            d = load_data()
            d[idx][6] = "Done"
            save_data(d)
            popup.destroy()
            set_content(random.choice(CHEERS))
            refresh_status()
        return do_finish

    for item in todo:
        idx = item[0]
        label_text = item[1] + " | " + item[2]
        ctk.CTkButton(popup, text=label_text, command=make_finish(idx)).pack(pady=4)


#buttons
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Add", command=open_add_window).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Schedule", command=show_schedule).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Search", command=open_search_window).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Finish", command=open_finish_window).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Pep talk", command=show_pep_talk).pack(side="left", padx=5)




refresh_status()
show_schedule()
window.mainloop()