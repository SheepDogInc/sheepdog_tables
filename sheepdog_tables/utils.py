class MockQuerySet(object):
    """
    MockQuerySet makes a list of dictionaries look like a queryset, providing
    several necessary functions without breaking anything.

    The idea here is that the get_table_qs method of :py:class:`sheepdog_tables.mixins.TablesMixin` should return
    one of these objects when you are using a dictionary based representation
    of data.

    :param dict_list: A list of dictionaries to wrap.
    """

    def __init__(self, dict_list):
        self.dict_list = dict_list

    def all(self):
        """
        Wrapper function for all()

        :return: :py:class:`MockQuerySet` of all dicts.
        """
        return MockQuerySet(self.dict_list)

    def __len__(self):
        """
        Wrapper function for len() and so on.

        :return: The length of :py:attr:`dict_list`
        """
        return len(self.dict_list)

    def __getitem__(self, n):
        """
        Wrapper function for iteration

        :param n: The index to access.
        :returns: The nth member of :py:attr:`dict_list`
        """
        return self.dict_list[n]
