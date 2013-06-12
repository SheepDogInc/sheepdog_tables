from django.core.paginator import Paginator


class NamespacedPaginator(Paginator):

    """
        Add simple namespacing to the default django Paginator
        and adding pagination helpers
    """
    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True, namespace=None, current_page=1):

        super(NamespacedPaginator, self).__init__(
            object_list, per_page, orphans, allow_empty_first_page)

        self.ns = namespace
        self.current_page = int(current_page)

    def pages(self):
        """
        returns a list of pages that the template can understand to render
        itself correctly.
        """
        all_pages = self._get_page_range()
        if len(all_pages) <= 10:
            return all_pages
        else:
            start = max(self.current_page - 4, 1)
            end = min(start + 8, len(all_pages))
            if start == 1:
                return all_pages[0:end + 1] + [None]
            elif end == len(all_pages):
                return [None] + all_pages[-9:]
            else:
                return [None] + all_pages[start - 1:end] + [None]


class MockPage(object):

    def __init__(self, object_list):
        self.object_list = object_list
