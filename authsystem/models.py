from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from datetime import datetime,timedelta

# Create your models here.

class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_student = models.BooleanField('Is student', default=False)
    is_teacher = models.BooleanField('Is teacher', default=False)

    





class UserExtend(models.Model):
    user2 = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField()
    def __str__(self):
       return self.user2.username
    
    
class AddBook(models.Model):
    user2 = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    bookid=CharField(max_length=10)
    bookname=CharField(max_length=50)
    subject=CharField(max_length=20)
    category= models.CharField(max_length = 10)
    sem = models.CharField(max_length=10, default='N/A')
    is_reserved = models.CharField(max_length=50)
    Brequest = models.CharField(max_length=50)
    #is_reserved=False
    #if is_reserved == True:
        #reserved_status = "Reserved"
    #else:
        #reserved_status = "Not Reserved" 
    def __str__(self):
        return str(self.bookname)+"["+str(self.bookid)+']'
def expiry():
    return datetime.today() + timedelta(days=15)

def is_available_for_reservation(self):
    return self.category == 'Not-Issued'



class IssueBook(models.Model):
    user2 = models.ForeignKey(User,on_delete=models.CASCADE)
    studentid=CharField(max_length=20)
    book1=models.CharField(max_length=20)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=expiry)
    def __str__(self):
        return self.studentid
    


class ReturnBook(models.Model):
    user2=models.ForeignKey(User,on_delete=models.CASCADE)
    bookid2=models.CharField(max_length=20)


class AddStudent(models.Model):
    user2=models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    sname=models.CharField(max_length=30)
    studentid=models.CharField(max_length=20)
    def __str__(self):
        return self.sname+'['+str(self.studentid)+']'
    





class ReservedBook(models.Model):
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,default=User.objects.first().id)
    studentid=CharField(max_length=20)
    book1=models.CharField(max_length=20)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=expiry)
    def __str__(self):
        return self.studentid
    
    
class BorrowBook(models.Model):
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,default=User.objects.first().id)
    studentid=CharField(max_length=20)
    book1=models.CharField(max_length=20)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=expiry)
    def __str__(self):
        return self.studentid
    


"""class RenewBook(models.Model):
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,default=User.objects.first().id)
    studentid=CharField(max_length=20)
    book1=models.CharField(max_length=20)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=expiry)
    def __str__(self):
        return self.studentid
    """



class TimeSlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.start_time} to {self.end_time}"
    




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    review_text = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.book_name}"