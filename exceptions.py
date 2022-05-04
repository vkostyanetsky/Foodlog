class CatalogEntryNotFound(Exception):
    pass

    def __init__(self, entry_title):

        self.message = "Catalog's entry \"{}\" is not found.".format(entry_title)

        super().__init__(self.message)


class CatalogNotFound(Exception):

    def __init__(self, path):

        self.message = "Catalog's file \"{}\" is not found.".format(path)

        super().__init__(self.message)