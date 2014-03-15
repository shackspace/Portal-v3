import db_actions


def list_users():
    cur, conn = db_actions.get_db()
    user_list = cur.execute("SELECT serial, name, surname, nick, firstValid, \
                             lastValid FROM user")

    output_list = [["Nr.", "First Name", "Last Name", "Nick", "Valid from", \
                    "Valid to"]]
    
    for result in user_list:
        output_list.append(result)

    pretty_print(output_list)


def pretty_print(output_list)
    col_width = [max(len(x) for x in col) for col in zip(*output_list)]

    for line in output_list:
        print "| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |"
