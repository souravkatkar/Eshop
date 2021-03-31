from django.db import models

class Customer(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email = self.email ):
            return True
        return False

    @staticmethod
    def get_by_email(email):
        try:
            return Customer.objects.get(email = email)

        except:
            return False