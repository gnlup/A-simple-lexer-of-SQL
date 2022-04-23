class Token_Seq(object):
    def __init__(self, token_name=None, token_type=None, token_value=None, line_index=1):
        self.token_name = token_name
        self.token_type = token_type
        self.token_value = token_value
        self.line_index = line_index

    def __str__(self):
        return '%-4s %-15s  <%s,%s>' % (self.line_index, self.token_name, self.token_type, self.token_value)



