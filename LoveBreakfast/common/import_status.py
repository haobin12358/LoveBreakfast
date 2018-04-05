# *- coding:utf8 *-

def import_status(msg, sta, code):
    from config import message, status, statuscode
    return eval("message.{0}, status.{1}, statuscode.{2}".format(msg, sta, code))
