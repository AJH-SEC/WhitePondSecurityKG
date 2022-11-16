from datetime import datetime,timezone,timedelta


def trans_time_zone(time_str):
    given_datetime = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    given_datetime_by_tzinfo = given_datetime.replace(tzinfo=timezone.utc)
    new_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return given_datetime_by_tzinfo.astimezone(timezone(timedelta(hours=8))).strftime(new_format)