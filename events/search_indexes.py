# events/search_indexes.py
from haystack import indexes
from .models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Event
