def build_cls_name(path=None, display_name=None, force_path=False):
    identifier = display_name
    if display_name == None or force_path == True:
        identifier = path

        if path == None:
            raise Exception("No class name could be determined")

    if identifier.startswith('/') or identifier.startswith('\\'):
        identifier = identifier[1:]

    if identifier.startswith('{'):
        identifier = identifier[1:]

    if identifier.endswith('}'):
        identifier = identifier[:-1]

    identifier = identifier.replace("/", "_")
    identifier = identifier.replace(" ", "_")
    identifier = identifier.replace("\\", "_")
    identifier = identifier.replace("{", "_")
    identifier = identifier.replace("}", "_")
    identifier = identifier.replace("-", "_")
    identifier = identifier.replace("$", "_")
    identifier = identifier.replace("~", "_")
    identifier = identifier.replace("=", "_")
    identifier = identifier.replace(".", "_")
    identifier = identifier.replace(":", "_")

    if identifier == 'import':
        identifier += 'x'

    if identifier == '' or None:
        identifier = 'unassigned'

    return identifier