from Fav_athls import Favourite


def is_data_correct(first_last_name):
    try:
        text_input_name = (first_last_name.partition(" "))[2]
        text_input_last_name = (first_last_name.partition(" "))[0]
        temp_fav_obj = Favourite()
        temp_fav_obj.encode(text_input_name + " " + text_input_last_name)
        temp_fav_obj.find_in_PZLA()
        temp_fav_obj.get_athl_site()
        return True
    except:
        return False
