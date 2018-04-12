# *- coding:utf8 *-

def import_status(msg, sta, code):
    from config import messages, status, status_code
    return eval("messages.{0}, status.{1}, status_code.{2}".format(msg, sta, code))
