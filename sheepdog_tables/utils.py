class MockQuerySet(object):
    """
    MockQuerySet makes a list of dictionaries look like a queryset, providing
    several necessary functions without breaking anything.

    The idea here is that the get_table_qs method of TablesMixin should return
    one of these objects when you are using a dictionary based representation
    of data.

    :params

    dict_list --  a list of dictionaries
    """
    def __init__(self, dict_list):
        self.dict_list = dict_list

    def all(self):
        return MockQuerySet(self.dict_list)

    def __len__(self):
        return len(self.dict_list)

    def __getitem__(self, n):
        return self.dict_list[n]
