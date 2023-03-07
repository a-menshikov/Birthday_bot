import datetime
import pytz

private_sub = 'private'
private_sub_description = 'добавленные пользователем дни рождения'
private_button = 'Персональная'
cf_sub = 'cf'
cf_sub_description = 'дни рождения ЦФ'
cf_button = 'ЦФ'

SUB_KIND = {
    private_sub: private_sub_description,
    cf_sub: cf_sub_description,
}

SUB_BUTTON_NAME = {
    private_sub: private_button,
    cf_sub: cf_button,
}

timezone_moscow = pytz.timezone("Etc/GMT-3")
today_full_date = datetime.datetime.now(timezone_moscow).date()
today_day = today_full_date.day
today_month = today_full_date.month
