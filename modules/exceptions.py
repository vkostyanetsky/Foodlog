class FoodDiaryException(Exception):
    pass


class CatalogEntryNotFound(FoodDiaryException):

    def __init__(self, entry_title):

        self.message = 'Catalog entry "{}" is not found.'.format(entry_title)

        super().__init__(self.message)
