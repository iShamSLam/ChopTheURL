from django.db import models


# model for database
# sync by --run syncdb
class Link(models.Model):
    orig_link = models.CharField(max_length=200)
    tiny_link = models.CharField(max_length=50, unique=True)
    follow_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.tiny_link
