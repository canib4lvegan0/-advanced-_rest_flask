
def convert_to_dec_or_alpha(param):

    if param.isdecimal():
        return int(param)
    elif (len(splitted_name := param.split('_')) > 1 and
          splitted_name[0].isalnum() and
          splitted_name[1].isalnum()) or param.isalnum():
        return param

    return None
