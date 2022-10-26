from tkinter import *
from tkinter import messagebox
from password_generator import PasswordGenerator
import json


class PasswordManager(Tk):

    def __init__(self):
        super(PasswordManager, self).__init__()
        self.data = DataModel(self)

        self.title("Password Manager")
        self.config(padx=50, pady=50)
        self.canvas_placeholder = Label(text="Canvas")
        self.canvas_placeholder.grid(row=0, column=1)

        self.website_label = Label(text="Website:")
        self.email_label = Label(text="Email/Username:")
        self.password_label = Label(text="Password:")

        self.website_label.grid(row=1, column=0)
        self.email_label.grid(row=2, column=0)
        self.password_label.grid(row=3, column=0)

        self.website_entry = Entry(width=21)
        self.email_entry = Entry(width=41)
        self.password_entry = Entry(width=21)

        self.website_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1, columnspan=2)
        self.password_entry.grid(row=3, column=1)

        self.generate_button = Button(text="Generate Password", command=self.data.generate_password)
        self.add_button = Button(text="Add", width=35, command=self.confirm_save)
        self.search_button = Button(text="Search", command=self.data.search_json, width=15)

        self.generate_button.grid(row=3, column=2)
        self.add_button.grid(row=4, column=1, columnspan=2)
        self.search_button.grid(row=1, column=2)

        self.website_entry.focus()
        self.email_entry.insert(0, "email@default.com")

        self.mainloop()

    def confirm_save(self):
        if len(self.email_entry.get()) == 0 or len(self.website_entry.get()) == 0 or\
                                                len(self.password_entry.get()) == 0:
            messagebox.showerror(title="Error", message="Please make sure you haven't left any fields empty.")
            return

        is_ok = messagebox.askokcancel(title=self.website_entry.get(),
                                       message=f"These are the credentials you entered. Save?\n\n"
                                       f"Email: {self.email_entry.get()}\n"
                                       f"Password: {self.password_entry.get()}")
        if is_ok:
            self.data.save_data()

    def clear_entries(self):
        self.website_entry.delete(0, END)
        self.password_entry.delete(0, END)

    @staticmethod
    def search_result_success(website, credentials):
        message = f"Your credentials for {website} are:\n\n"
        for email in credentials:
            message += f"Email: {email}\nPassword: {credentials[email]['password']}\n\n"
        messagebox.showinfo(title=website, message=message)

    @staticmethod
    def search_result_failure(error_text):
        messagebox.showerror(title="Error", message=error_text)


class DataModel:

    def __init__(self, ui: PasswordManager):
        self.path = "./data.json"
        self.ui = ui
        self.generator = PasswordGenerator()

    def save_data(self):
        website = self.ui.website_entry.get()
        email = self.ui.email_entry.get()
        password = self.ui.password_entry.get()
        new_data = {
            website: {
                email: {
                    'password': password
                }
            }
        }

        try:
            with open(self.path, "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        if website in data.keys():
            data[website][email] = {"password": password}
        else:
            data.update(new_data)

        with open(self.path, "w") as data_file:
            json.dump(data, data_file, indent=4)

        self.ui.clear_entries()

    def generate_password(self):
        self.ui.password_entry.delete(0, END)
        password = self.generator.get_password()
        self.ui.password_entry.insert(0, password)

    def search_json(self):
        target_website = self.ui.website_entry.get()
        if len(target_website) == 0:
            self.ui.search_result_failure("Please enter a website name.")
            return

        try:
            with open(self.path, "r") as data_file:
                data = json.load(data_file)
                credentials = data[target_website]
            self.ui.search_result_success(target_website, credentials)
        except FileNotFoundError:
            self.ui.search_result_failure("data.json file not found.")
        except KeyError:
            self.ui.search_result_failure(f'No credentials for "{target_website}" exist.')


def main():
    PasswordManager()


if __name__ == '__main__':
    main()
