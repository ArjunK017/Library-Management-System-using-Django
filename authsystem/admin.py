from django.contrib import admin
from .models import User
from django.contrib.sessions.models import Session
from .models import UserExtend
from .models import AddBook,IssueBook,ReturnBook,AddStudent,ReservedBook,BorrowBook


# Register your models here.
admin.site.register(User)

admin.site.register(Session)

admin.site.register(UserExtend)

admin.site.register(BorrowBook)

admin.site.register(ReservedBook)


class AddBook_Admin(admin.ModelAdmin):
    list_display=("user2","bookid","bookname","subject","category")
admin.site.register(AddBook,AddBook_Admin)
class IssueBookAdmin(admin.ModelAdmin):
    list_display=("user2","book1","studentid")
admin.site.register(IssueBook,IssueBookAdmin)
class ReturnBookAdmin(admin.ModelAdmin):
    list_display=("user2","bookid2")
admin.site.register(ReturnBook,ReturnBookAdmin)
class AddStudentAdmin(admin.ModelAdmin):
    list_display=("user2","sname","studentid")
admin.site.register(AddStudent,AddStudentAdmin)