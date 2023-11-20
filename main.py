import json
from tkinter import *
from tkinter import messagebox
from random import shuffle, choice, randint
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [(choice(letters)) for _ in range(randint(8, 10))]
    password_list += [(choice(symbols)) for _ in range(randint(2, 4))]
    password_list += [(choice(numbers)) for _ in range(randint(2, 4))]
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = web_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    datas = {website: {
        "Email": email,
        "Password": password,
    }}
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data:
                data_file = json.load(data)
        except FileNotFoundError:
            with open("data.json", "w") as data:
                json.dump(datas, data, indent=4)
        else:
            data_file.update(datas)
            with open("data.json", "w") as data:
                json.dump(data_file, data, indent=4)
        finally:
            web_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    search_key = web_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Data file not found", message="No passwords have been saved."
                                                                  " Please save some passwords and try again")
    else:
        if search_key not in data:
            messagebox.showerror(title="Error", message=f"No details for the website {search_key} found.")
        else:
            messagebox.showinfo(title=search_key, message=f"Email: {data[search_key]['Email']}"
                                                          f"\nPassword: {data[search_key]['Password']}")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

web_entry = Entry(width=30)
web_entry.grid(column=1, row=1, sticky="W")
web_entry.focus()

search_button = Button(text="Search", width=18, command=search_password)
search_button.grid(column=2, row=1, sticky="E")

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry()
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(END, "test@gmail.com")
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky="W")

gen_button = Button(text="Generate Password", width=18, command=generate_password)
gen_button.grid(column=2, row=3, sticky="E")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
