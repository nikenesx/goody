from django.db import models
from django.contrib.auth.models import User
import re
from datetime import datetime


class Specialty(models.Model):

    specialty_name = models.CharField(max_length=50)

    def __str__(self):
        return self.specialty_name


class Doctor(models.Model):

    doctor_name = models.CharField(max_length=50)
    specialty = models.ManyToManyField(Specialty)

    def __str__(self):
        return self.doctor_name


class Review(models.Model):

    review_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    review_update_date = models.DateTimeField(auto_now=True)
    original_rev_text = models.TextField()
    processed_rev_text = models.TextField()
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def remake_rev(self):
        review_text = self.original_rev_text.strip()
        review_text = re.sub(r'\s+', ' ', review_text)
        punctuation = ['.', '!', ',', ';', ':', '?']
        review_text += '  '
        upper_count = 1
        flag = False
        temp_text = ''
        for i in range(len(review_text) - 1):
            if review_text[i] in punctuation and review_text[i] == review_text[i + 1]:
                continue
            if review_text[i] == ' ' and review_text[i + 1] in punctuation:
                continue
            if review_text[i].isupper() and review_text[i + 1].isupper():
                upper_count += 1
            else:
                upper_count = 1
            if upper_count > 5:
                flag = True
            if review_text[i] in punctuation and review_text[i + 1] != ' ':
                temp_text += review_text[i] + ' '
                continue
            if review_text[i] in punctuation and review_text[i + 1] == ' ' and review_text[i + 2] in punctuation:
                temp_text += review_text[i] + ' '
                continue

            temp_text += review_text[i]

        if flag:
            result_review = ''
            temp_sent = ''
            for i in range(len(temp_text)):
                if temp_text[i] in ('.', '?', '!'):
                    if temp_sent != '' and temp_sent[0] == ' ':
                        result_review += ' ' + temp_sent[1:].capitalize() + temp_text[i]
                    else:
                        result_review += temp_sent.capitalize() + temp_text[i]
                    temp_sent = ''
                else:
                    temp_sent += temp_text[i]
            return result_review + temp_sent[:-1]

        return temp_text[:-1]


class CurseWord(models.Model):

    word = models.CharField(max_length=30)

    def __str__(self):
        return self.word


class ExceptionWord(models.Model):

    word = models.CharField(max_length=30)

    def __str__(self):
        return self.word
