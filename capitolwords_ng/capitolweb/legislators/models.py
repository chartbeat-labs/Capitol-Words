from django.db import models


class State(models.Model):
    def __str__(self):
        return self.name

    short = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=25, unique=True)


class CongressPerson(models.Model):
    def __str__(self):
        return self.official_full

    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    suffix = models.CharField(max_length=5)
    nickname = models.CharField(max_length=25)
    official_full = models.CharField(max_length=50, unique=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=(('M', "Male"), ('F', 'Female')))
    religion = models.CharField(max_length=30)


class Term(models.Model):
    person = models.ForeignKey(CongressPerson, on_delete=models.CASCADE, related_name='terms')
    type = models.CharField(max_length=1, choices=(('sen', "Senate"), ('rep', 'House')))
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.ForeignKey(State)
    district = models.IntegerField(default=-1)
    election_class = models.CharField(max_length=1)
    state_rank = models.CharField(max_length=6, choices=(('junior', 'junior'), ('senior', 'Senior')))
    party = models.CharField(max_length=25)
    caucus = models.CharField(max_length=25)
    address = models.TextField()
    office = models.TextField()
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    contact_form = models.URLField()
    rss_url = models.URLField
    url = models.URLField()


class ExternalId(models.Model):
    person = models.ForeignKey(CongressPerson, on_delete=models.CASCADE, related_name='external_ids')
    type = models.CharField(max_length=50)
    value = models.CharField(max_length=50)



