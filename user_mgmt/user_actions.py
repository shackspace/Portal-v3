import db_actions


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


def pretty_print(output_list):
    col_width = [max(len(str(x)) for x in col) for col in zip(*output_list)]

    for line in output_list:
        print "| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |"
