from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Language(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Point(models.Model):
    explanation = models.TextField(max_length=50)
    notes = models.TextField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # element_list = db.relationship('Element', backref='point', lazy=True)
    # category_list = db.relationship('Category', backref='point', lazy=True)
    def __str__(self):
        return f"{self.explanation}"

# Thinking that a table for elements with point_id as the foreign key will be better appoarch
# Will keep this just in case I like it better

class Element(models.Model):
    point_id = models.ForeignKey(Point, on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    type = models.CharField(max_length=8)