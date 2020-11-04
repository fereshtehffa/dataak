from django.db import models


#TODO classes need to be reafctor: abstract class needed for redundant rows such az url


class Community(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)


class Thread(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey("User", on_delete=models.SET_NULL, blank=True, null=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)


class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True, null=True)