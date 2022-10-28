import re
from hw_10 import *

CONTACTS = AddressBook()


def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except (ValueError, IndexError, UnboundLocalError):
            print("Error. Give me correct name, phone or birthday, please")
        except KeyError:
            print("Error. Enter user name, please")
    return wrapper


def hello_handler():
    print("How can I help you?")


def quit_handler():
    print("Good bye!")
    CONTACTS.save_contacts()
    quit()


@input_error
def add_contact_handler(var):
    name = var.split()[1]
    phone = var.split()[2]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.add_phone(phone)
    else:
        record = Record(name, phone)
        CONTACTS.add_record(record)
    print("New contact was added")


@input_error
def find_contact_handler(var):
    for name, record in CONTACTS.items():
        if name == var.split()[1]:
            print(f"{name.capitalize()}: {[phone.value for phone in record.phones]}")


@input_error
def delete_contact_handler(var):
    name = var.split()[1]
    phone_for_delete = var.split()[2]
    record = CONTACTS.data[name]
    record.delete_phone(phone_for_delete)
    print("Contact's phone was deleted")


@input_error
def change_contact_handler(var):
    name = var.split()[1]
    phone_for_change = var.split()[2]
    new_phone = var.split()[3]
    if phone_for_change and new_phone:
        record = CONTACTS.data[name]
        record.change_phone(phone_for_change, new_phone)
        print("Contact was changed")


@input_error
def add_birthday_handler(var):
    name = var.split()[2]
    birthday = var.split()[3]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        if record.birthday == "":
            record.add_birthday(birthday)
            print("Contact's birthday was added")
        else:
            print("Contact's birthday was added before")


@input_error
def days_to_birthday_handler(var):
    name = var.split()[0]
    if name in CONTACTS:
        record = CONTACTS.data[name]
        record.days_to_birthday()


def show_contacts_handler():
    for name, record in CONTACTS.items():
        if record.birthday != "":
            print("{:<10}{:^35}{:>10}".format(name.capitalize(), " ".join([phone.value for phone in record.phones]), record.birthday))
        else:
            print("{:<10}{:^35}{:>10}".format(name.capitalize(), " ".join([phone.value for phone in record.phones]), "-"))


def iteration():
    for i in CONTACTS.iterator():
        print(i)


def find(var):
    show_list = []
    for name, record in CONTACTS.items():
        if re.search(var, name):
            show_list.append(f"{name.capitalize()}: {[phone.value for phone in record.phones]}")
        for phone in record.phones:
            if re.search(var, phone.value):
                show_list.append(f"{name.capitalize()}: {[phone.value for phone in record.phones]}")
    if show_list == []:
        raise Exception
    print(f"You are looking for '{var}', the most suitable result is: {show_list}")


COMMANDS = {
    "hello": hello_handler,
    "show all": show_contacts_handler,
    "exit": quit_handler,
    "close": quit_handler,
    "good bye": quit_handler,
    "iter": iteration
}


def main():
    while True:
        var = (input("Enter command: ")).lower()
        if var.startswith('add birthday'):
            add_birthday_handler(var)
        elif var.endswith("birthday"):
            days_to_birthday_handler(var)
        elif var.startswith('add'):
            add_contact_handler(var)
        elif var.startswith('change'):
            change_contact_handler(var)
        elif var.startswith('phone'):
            find_contact_handler(var)
        elif var.startswith('delete'):
            delete_contact_handler(var)
        elif var in COMMANDS:
            COMMANDS[var]()
        else:          
            try:
                find(var)
            except:
                print("Wrong command!")
            continue



if __name__ == "__main__":
    main()