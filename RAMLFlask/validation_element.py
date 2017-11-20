class Validation_Element(object):
    """Validation object for usage in specifying validation requirements in generated code"""

    def __init__(self, source, name, desc, val_type, enum, pattern, min_length, max_length, minimum, maximum, example, repeat, required, default):
        self.source = source
        self.name = name
        self.desc = desc
        self.val_type = val_type
        self.enum = enum
        self.pattern = pattern
        self.min_length = min_length
        self.max_length = max_length
        self.minimum = minimum
        self.maximum = maximum
        self.example = example
        self.repeat = repeat
        self.required = required
        self.default = default

    def dump(self):
        return {
            'source': self.source,
            'validation': {
            'name': self.name,
            'desc': self.desc,
            'type': self.val_type,
            'enum': self.enum,
            'pattern': self.pattern,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'example': self.example,
            'repeat': self.repeat,
            'required': self.required,
            'default': self.default
        }}
