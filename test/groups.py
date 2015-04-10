LAYOUT = "LAYOUT"

def groups(*group_list):
    """Decorator that adds group name to test method for use with the attributes (-A) plugin.
    """
    def wrap_ob(ob):
        if len(group_list) == 1:
            setattr(ob, "group", group_list[0])
        elif len(group_list) > 1:
            setattr(ob, "groups", group_list)
        return ob
    return wrap_ob
