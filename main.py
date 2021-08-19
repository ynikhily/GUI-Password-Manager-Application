from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
               'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letter + password_symbol + password_number

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(END, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def search_password():
    try:
        with open('data.json', mode='r') as file:
            data = json.load(file)

    except FileNotFoundError and ValueError:
        messagebox.showerror(title="Error!!", message="No Password data file or entries in file found!")

    else:
        website = website_entry.get().lower()

        if website == '':
            messagebox.showerror(title="Error!!", message="Please do not leave the website box empty")
        else:
            try:
                email = data[website]['email']
                password = data[website]['password']

            except KeyError:
                messagebox.showerror(title="Error!!", message=f"No Entries found for {website} website.")

            else:
                messagebox.showinfo(title="Gotcha!!", message=f"Email: {email}\nPassword: {password}")


def write_to_file(content):
    with open('data.json', mode='w') as file:
        json.dump(content, file, indent=4)


def save_entries():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email,
                          "password": password}}

    if website == '' or email == '' or password == '':
        messagebox.showerror(title='Error', message='Please do not leave any empty fields')

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"You have entered the following information"
                                                              f"\nEmail: {email}\nPassword: {password}\n"
                                                              f"Are you sure you want to add this info?")

        if is_ok:

            try:
                with open('data.json', mode='r') as file:
                    data = json.load(file)

            except FileNotFoundError:
                write_to_file(new_data)

            else:
                data.update(new_data)
                write_to_file(data)

            website_entry.delete(0, END)
            password_entry.delete(0, END)

            messagebox.showinfo(title="Info", message="Entries have been added to your password manager file.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("My Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

website_entry = Entry(width=34)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(END, 'someemail@xyz.com')

password_entry = Entry(width=34)
password_entry.grid(row=3, column=1)

add_button = Button(text='Add', width=44, command=save_entries)
add_button.grid(row=4, column=1, columnspan=2)

generate_button = Button(text='Generate Password', command=generate_password)
generate_button.grid(row=3, column=2)

search_button = Button(text='Search', width=15, command=search_password)
search_button.grid(row=1, column=2)

window.mainloop()
