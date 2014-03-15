import db_actions
import subprocess


def list_users():
    cur, conn = db_actions.get_db()
    user_list = cur.execute("SELECT serial, name, surname, nickname, firstValid, \
                             lastValid FROM user")

    output_list = [["Nr.", "First Name", "Last Name", "Nick", "Valid from", \
                    "Valid to"]]
    
    for result in user_list:
        output_list.append(result)

    conn.close()

    if len(output_list) > 1:
        pretty_print(output_list)
    else:
        print("No users in database.")


def del_user(uid):
    cur, conn = db_actions.get_db()
    user = cur.execute("SELECT name, surname, nickname FROM user\
                        WHERE serial = ?", (uid, )).fetchall()[0]
    
    if len(user) == 0:
        print("User not found.")
    else:
        question = "Do you want to delete " + user[0] + " " + user[1] 
        question += " (nick: " + user[2] + ")? [y/n] " if user[2] else "? [y/n] "

        if raw_input(question).lower() == 'y':
            cur.execute("DELETE FROM user WHERE serial = ?", (uid, ))
            conn.commit()
            conn.close()
            print("User successfully deleted.")
        else:
            conn.close()
            print("User not deleted.")


def add_user(serial, keyfile, name, surname, nickname, lastValid, firstValid):
    cur, conn = db_actions.get_db()

    if not (serial and keyfile and name and surname):
        print("You must provide a membership number, a name, a surname and\
               a keyfile.")
        sys.exit(1)

    if not is_key_valid(keyfile):
        print("Please provide a valid keyfile.")
        sys.exit(1)

    try:
        cur.execute("INSERT INTO user(serial, name, surname, firstValid, \
                     lastValid, pubkey, nickname) VALUES (?, ?, ?, ?, ?, ?, ?)",\
                     (serial, name, surname, firstValid, lastValid, \
                     get_key(keyfile), nickname))
        conn.commit()
        conn.close()
        print("User successfully added.")
    
    except:
        conn.close()
        print("Could not add user.")


def pretty_print(output_list):
    col_width = [max(len(str(x)) for x in col) for col in zip(*output_list)]

    for line in output_list:
        print "| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |"


def get_key(keyfile):
    f = open(keyfile, 'r')
    key = f.read()
    f.close()

    key = key.strip()
    return key


def is_key_valid(keyfile):
    try:
        subprocess.check_call(["ssh-keygen", "-l", "-f", str(keyfile)])
        return True
    except subprocess.CalledProcessError:
        return False

