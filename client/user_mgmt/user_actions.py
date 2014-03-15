from user_mgmt import db_actions
import subprocess
import sys
import sqlite3


def list_users():
    """Gives a user list, fails if no database exists"""
    cur, conn = db_actions.get_db()
    user_list = cur.execute("SELECT serial, name, surname, nickname, " +
                                 "firstValid, lastValid FROM user")

    output_list = [["Nr.", "First Name", "Last Name", "Nick", "Valid from", \
                    "Valid to"]]
    for result in user_list:
        output_list.append(result)

    conn.close()

    if len(output_list) > 1:
        pretty_print(output_list)
    else:
        print "No users in database."


def del_user(uid):
    """Deletes a user given his user ID"""
    cur, conn = db_actions.get_db()
    user = cur.execute("SELECT name, surname, nickname FROM user\
                        WHERE serial = ?", (uid, )).fetchall()[0]

    if len(user) == 0:
        print "User not found."

    else:
        question = "Do you want to delete " + user[0] + " " + user[1]
        question += " (nick: " + user[2] + ")" if user[2] else ""
        question += "? [y/n] "

        if raw_input(question).lower() == 'y':
            cur.execute("DELETE FROM user WHERE serial = ?", (uid, ))
            conn.commit()
            conn.close()
            print "User successfully deleted."

        else:
            conn.close()
            print "User not deleted."


def add_user(serial, keyfile, name, surname, nickname, lastValid, firstValid):
    """adds a user, needs at least a serial number, name, surname and keyfile
    writes to an sql database, fails if the database doesn't exist'"""
    cur, conn = db_actions.get_db()

    if not (serial and keyfile and name and surname):
        print("You must provide a membership number (-u), a name (-n),"
                + " a surname (-s) and a keyfile (-k).")
        sys.exit(1)

    if not is_key_valid(keyfile):
        print "Please provide a valid keyfile."
        sys.exit(1)

    try:
        cur.execute("INSERT INTO user(serial, name, surname, firstValid, \
                     lastValid, pubkey, nickname) VALUES (?,?,?,?,?,?,?)",\
                     (serial, name, surname, firstValid, lastValid, \
                     get_key(keyfile), nickname))
        conn.commit()
        conn.close()
        print "User successfully added."

    except sqlite3.IntegrityError as err:
        conn.close()
        print "Could not add user:" , err


def mod_user(uid, options, args):
    """adds a user, needs at least a serial number, name, surname and keyfile
    writes to an sql database, fails if the database doesn't exist'"""
    cur, conn = db_actions.get_db()
    fields = []
    values = []
    options = vars(options)

    for key in options.keys():
        if options[key]:
            fields.append(key)
            values.append(options[key])

    values.append(uid)

    if len(fields) == 0:
        print("Nothing's changed!")
        sys.exit(0)

    user = cur.execute("SELECT name, surname, nickname FROM user\
                        WHERE serial = ?", (uid, )).fetchall()[0]

    if len(user) == 0:
        print "User not found."
        sys.exit(1)

    else:
        change_list = [t[0] + " to " + t[1] for t in zip(fields, values)]
        question = "Do you want to modify " + user[0] + " " + user[1]
        question += " (nick: " + user[2] + ")" if user[2] else ""
        question += "? [y/n]\nThe following fields will be changed: "
        question += ", ".join(change_list) + ". "

        if 'keyfile' in fields and not is_valid_key(options.keyfile):
            print "This file doesn't contain a valid public key'"
            sys.exit(1)

        if raw_input(question).lower() == 'y':
            mod = "UPDATE user SET "
            mod += ",".join(field + "= ? " for field in fields)
            mod += " WHERE serial = ?"

            cur.execute(mod, values)
            conn.commit()
            conn.close()


def pretty_print(output_list):
    """prints a pretty list to stdout"""
    col_width = [max(len(str(x)) for x in col) for col in zip(*output_list)]

    for line in output_list:
        print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                        for i, x in enumerate(line)) + " |")


def get_key(keyfile):
    """reads a public key from a file, strips leading and trailing
    whitespace"""
    f = open(keyfile, 'r')
    key = f.read()
    f.close()

    key = key.strip()
    return key


def is_key_valid(keyfile):
    """checks if a given keyfile contains a valid public key"""
    try:
        subprocess.check_call(["ssh-keygen", "-l", "-f", str(keyfile)])
        return True
    except subprocess.CalledProcessError:
        return False

