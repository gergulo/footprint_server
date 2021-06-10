from datetime import datetime, timedelta

"""
各种辅助
"""


def parse_duration(seconds):
    """
    秒转为时长
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    lst = []
    if h != 0:
        lst.append("%01d小时" % h)
    if m != 0:
        lst.append("%01d分" % m)
    if s != 0:
        lst.append("%01d秒" % s)

    return "".join(lst)


def fetchall_dict(cursor):
    """
    Return all rows from a cursor as a dict
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def validate_datetime(datetime_text, datetime_format="%Y-%m-%d %H:%M:%S"):
    """
    检查是否有效日期字符串
    """
    try:
        datetime.strptime(datetime_text, datetime_format)
        return True
    except ValueError:
        return False


def get_client_ip(request):
    """
    获取客户端ip
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
        print("x_forwarded_for:{0}".format(ip))
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_last_day_of_month(any_date=None):
    """
    获取获得一个月中的最后一天
    :param any_date: 任意日期
    :return: string
    """
    if not any_date:
        any_date = get_day(datetime.now())
    next_month = any_date.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def get_first_day_of_month(any_date=None):
    """
    获取获得一个月中的第一一天
    :param any_date: 任意日期
    :return: string
    """
    if not any_date:
        any_date = get_day(datetime.now())
    return any_date - timedelta(days=any_date.day - 1)


def get_first_day_of_next_month(any_date=None):
    """
    获取获得下一个月中的第一天
    :param any_date: 任意日期
    :return: string
    """
    return get_last_day_of_month(any_date) + timedelta(days=1)


def get_day(any_date=None):
    if not any_date:
        any_date = datetime.now()
    return datetime.strptime(any_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
