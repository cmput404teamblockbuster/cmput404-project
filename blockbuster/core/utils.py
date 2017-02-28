def django_choice_options(dict_list, attribute):
    """
    converts a dict list to a list-of-list type that django choices require
    """
    return list((key, item[attribute]) for key, item in dict_list.items())

