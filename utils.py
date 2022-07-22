from typing import Dict, Union, List

ItemJSON = Dict[str, Union[int, str, float]]
StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]
UserJSON = Dict[str, Union[int, str, bool]]


def to_decimal_or_alpha(param):
    if param.isdecimal():
        return int(param)
    elif (
        len(splitted_name := param.split("_")) > 1
        and splitted_name[0].isalnum()
        and splitted_name[1].isalnum()
    ) or param.isalnum():
        return param

    return None
