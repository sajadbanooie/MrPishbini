from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    user_name = models.CharField(max_length=20, blank=True, null=True)
    id = models.IntegerField(primary_key=True, unique=True)

    score = models.IntegerField(default=0)

    def __str__(self):
        return "@" + str(self.id)


class Team(models.Model):
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=4)
    flag = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    teams = models.ManyToManyField(Team, max_length=2)
    time = models.DateTimeField()
    is_available = models.BooleanField()
    is_knockout = models.BooleanField()
    t1_goals = models.IntegerField(blank=True, null=True)
    t2_goals = models.IntegerField(blank=True, null=True)
    t1_pk_goals = models.IntegerField(blank=True, null=True)
    t2_pk_goals = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.teams.all()[0]) + "-" + str(self.teams.all()[1])


class Pishbini(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t1_goals = models.IntegerField()
    t2_goals = models.IntegerField()
    t1_pk_goals = models.IntegerField(blank=True, null=True)
    t2_pk_goals = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + ":" + str(self.match)

    class Meta:
        unique_together = ('match', 'user',)


class PrePishbini(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    winner = models.CharField(max_length=10)
    best_player = models.CharField(max_length=15)
    goal_winner = models.CharField(max_length=15)
    most_goals = models.IntegerField()
