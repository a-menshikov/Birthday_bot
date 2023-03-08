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

timezone = pytz.timezone("Etc/GMT-3")
