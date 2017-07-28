from django.db import models
from legislators.models import CongressPerson


class NamedEntity(models.Model):
    class Meta:
        verbose_name_plural = "namedentities"

    def __str__(self):
        return self.entity
    entity = models.CharField(max_length=25, unique=True)


class SearchTerm(models.Model):
    def __str__(self):
        return self.term
    term = models.CharField(max_length=25, unique=True)


class InterestingSearch(models.Model):
    class Meta:
        verbose_name_plural = "interestingsearches"

    def __str__(self):
        return self.name
    name = models.CharField(max_length=30, unique=True)
    entities = models.ManyToManyField(NamedEntity)
    search_terms = models.ManyToManyField(SearchTerm)


class FoundResult(models.Model):
    class Meta:
        unique_together = (("interesting_search", "speaker", "document_id"),)
    interesting_search = models.ForeignKey(InterestingSearch, on_delete=models.CASCADE)
    speaker = models.ForeignKey(CongressPerson, on_delete=models.CASCADE)
    document_id = models.CharField(max_length=100)
    document_date = models.DateField()
    document_title = models.CharField(max_length=255)
    fragment = models.TextField()

