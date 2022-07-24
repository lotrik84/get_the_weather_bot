
thunderstorm = '\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
drizzle = '\U0001F4A7'  # Code: 300's
rain = '\U0001F327'  # Code: 500's
snowflake = '\U00002744'  # Code: 600's snowflake
snowman = '\U000026C4'  # Code: 600's snowman, 903, 906
atmosphere = '\U0001F301'  # Code: 700's foogy
clearSky = '\U00002600'  # Code: 800 clear sky
fewClouds = '\U000026C5'  # Code: 801 sun behind clouds
clouds = '\U00002601'  # Code: 802-803-804 clouds general
hot = '\U0001F525'  # Code: 904
defaultEmoji = '\U0001F300'  # default emojis


def getemoji(weatherid):
    if weatherid:
        if str(weatherid)[0] == '2' or weatherid == 900 or weatherid == 901 or weatherid == 902 or weatherid == 905:
            return thunderstorm
        elif str(weatherid)[0] == '3':
            return drizzle
        elif str(weatherid)[0] == '5':
            return rain
        elif str(weatherid)[0] == '6' or weatherid == 903 or weatherid == 906:
            return snowflake + ' ' + snowman
        elif str(weatherid)[0] == '7':
            return atmosphere
        elif weatherid == 800:
            return clearSky
        elif weatherid == 801:
            return fewClouds
        elif weatherid == 802 or weatherid == 803 or weatherid == 804:
            return clouds
        elif weatherid == 904:
            return hot
        else:
            return defaultEmoji

    else:
        return defaultEmoji
