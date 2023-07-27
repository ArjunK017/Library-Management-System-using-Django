from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from .forms import SignUpForm, LoginForm, TimeSlotForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime,timedelta,date
from .models import IssueBook, UserExtend,AddBook,ReturnBook,AddStudent,ReservedBook,BorrowBook, TimeSlot, Review
from authsystem.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('adminpage')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                request.session['is_logged'] = True
                user = request.user.id 
                request.session["user_id"] = user
                return redirect('adminpage')
            elif user is not None and user.is_student:
                login(request, user)
                request.session['is_logged'] = True
                user = request.user.id
                return redirect('student')
            elif user is not None and user.is_teacher:
                login(request, user)
                request.session['is_logged'] = True
                user = request.user.id
                return redirect('teacher')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request,'admin.html')


def student(request):
    Book = AddBook.objects.all()
    return render(request,'student.html',{'Book':Book})


def teacher(request):
    Book = AddBook.objects.all()
    return render(request,'teacher.html',{'Book':Book})

def logout_view(request):
    return render(request, 'logout.html')
def snotification(request):
    return render(request, 'snotification.html')
def bookrenewal(request):
    return render(request, 'bookrenewal.html')
def s_about(request):
    return render(request, 's_about.html')
def s_reserved(request):
    return render(request, 's_reserve.html')
def s_borrowhistory(request):
    return render(request, 's_borrowhistory.html')
def s_profile(request):
    return render(request, 's_profile.html')
def contact(request):
    return render(request, 'contact.html')
def bookstats(request):
    return render(request, 'bookstats.html')
def bookupdate(request):
    return render(request,"bookupdate.html")

def s_borrowbook(request):
    return render(request, 's_borrowbook.html')

def fineimpo(request):
    return render(request, 'fineimpo.html')
def datamanip(request):
    return render(request, 'datamanipulation.html')

def dashboard(request):
    Book = AddBook.objects.all()
    return render(request,'dashboard.html',{'Book':Book})


def addbook(request):
    Book = AddBook.objects.all()
    return render(request,'addbook.html',{'Book':Book})

def AddBookSubmission(request):
    
    if request.method == "POST":
        bookid = request.POST["bookid"]
        bookname = request.POST["bookname"]
        subject = request.POST["subject"]
        category=request.POST["category"]
        sem=request.POST["sem"]
        add = AddBook(bookid=bookid,bookname=bookname,subject=subject,category=category,sem=sem,Brequest="0",is_reserved="0")
        add.save()
        Book = AddBook.objects.all()
        return render(request,'dashboard.html',{'Book':Book})
    return redirect('/')   


def deletebook(request,id):
    AddBook_info = AddBook.objects.get(id=id)
    AddBook_info.delete()
    return redirect("dashboard")


def bookissue(request):
    return render(request,'bookissue.html')


def returnbook(request):
    return render(request,'returnbook.html')

def issuebooksubmission(request):
    if request.method == 'POST':
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        studentid = request.POST['studentid']
        book1 = request.POST['book1']
        store = AddBook.objects.filter(bookid=book1)

        # Check the maximum number of issued books based on user role
        max_issued_books = 3 if user1.is_student else 4
        issued_books_count = IssueBook.objects.filter(user2=user1).count()

        if issued_books_count >= max_issued_books:
            messages.error(request, "Maximum number of issued books reached!")
        else:
            def get_category(addbook):
                if addbook.category == "Not-Issued":
                    addbook.category = "Issued"
                    obj = IssueBook(user2=user1, studentid=studentid, book1=book1)
                    obj.save()
                    addbook.save()
                elif addbook.category == "To-be-Issued":
                    addbook.is_reserved = "0"
                    addbook.category = "Issued"
                    obj = IssueBook(user2=user1, studentid=studentid, book1=book1)
                    obj.save()
                    addbook.save()
                elif addbook.category == "To-be-Reserved":
                    addbook.category = "Issued"
                    addbook.Brequest = studentid
                    addbook.is_reserved = "0"
                    addbook.Rrequest = "0"
                    obj = IssueBook(user2=user1, studentid=studentid, book1=book1)
                    obj.save()
                    addbook.save()
                else:
                    messages.error(request, "Book already issued!")

            category_list = list(set(map(get_category, store)))
        
        Issue = IssueBook.objects.all()
        return render(request, 'bookissue.html', {'Issue': Issue})
    
    return redirect('/')


def returnbooksubmission(request):
    if request.method=='POST':
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        bookid2=request.POST['bookid2']
        store1=AddBook.objects.filter(bookid=bookid2)
        def return_book(returnbook):
            if returnbook.category=="Issued":
                returnbook.category="Not-Issued"
                returnbook.Brequest="0"
                returnbook.is_reserved="0"
                returnbook.Rrequest="0"
                obj1=ReturnBook(user2=user1,bookid2=bookid2)
                obj=IssueBook.objects.filter(book1=bookid2)
                obj.delete()
                obj1.save()
                returnbook.save()
            else:
                messages.error(request," Book not  issued !!!")
        returncategorylist=list(set(map(return_book,store1)))
        Return= ReturnBook.objects.all()
        return render(request,'returnbook.html',{'Return':Return})
    return redirect('/')


def Search(request):
    query2=request.GET["query2"]
    Book=AddBook.objects.filter(bookid__icontains=query2)
    params={'Book':Book}
    return render(request,'dashboard.html',params)

"""def search_users(request):
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(userid__icontains=query)
        return render(request, 'viewstudents.html', {'users': users, 'query': query})
    else:
        return render(request, 'viewstudents.html')"""


def editbookdetails(request,id):
    Book = AddBook.objects.get(id=id)
    return render(request,'editdetails.html',{'Book':Book})

def updatedetails(request,id):
 
    if request.method=="POST":
        add=AddBook.objects.get(id=id)
        add.bookid=request.POST["bookid"]
        add.bookname=request.POST["bookname"]
        add.sem=request.POST["sem"]
        add.subject=request.POST["subject"]
        add.ContactNumber=request.POST['category']
        add.save()
    return redirect("dashboard")

"""def addstudent(request):
    return render(request,'addstudent.html')
"""
def viewstudents(request):
    students = User.objects.filter(is_admin=False)
    student_list = []
    for student in students:
        name = student.first_name + " " + student.last_name
        ID = student.username
        Email = student.email
        student_list.append({'name': name, 'ID': ID, 'Email': Email})
    return render(request, 'viewstudents.html', {'students': student_list})

    
def Searchstudent(request):
    query = request.GET.get("query")
    students = User.objects.filter(
        Q(username__icontains=query) & (Q(is_student=True) | Q(is_teacher=True))
    )
    student_list = []
    for student in students:
        name = student.first_name + " " + student.last_name
        ID = student.username
        Email = student.email
        student_list.append({'name': name, 'ID': ID, 'Email': Email})
    params1 = {'students': student_list, 'query': query}
    return render(request, 'viewstudents.html', params1)

"""def addstudentsubmission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            sname = request.POST["sname"]
            studentid = request.POST["studentid"]

            # Check if an AddStudent object already exists for the user
            existing_student = AddStudent.objects.filter(user2=user1).first()
            if existing_student:
                # Update the existing student's details
                existing_student.user2 = user1
                existing_student.sname = sname
                existing_student.studentid = studentid
                existing_student.save()
            else:

                # Create a new AddStudent object
                add = AddStudent(user2=user1, sname=sname, studentid=studentid)
                add.save()

        Student = AddStudent.objects.all()
        return render(request, 'addstudent.html', {'Student': Student})
    return redirect('/')   """


"""def addstudentsubmission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            sname = request.POST["sname"]
            studentid = request.POST["studentid"]

            # Check if an AddStudent object already exists for the user and studentid
            existing_student = AddStudent.objects.filter(user2=user1, studentid=studentid).first()
            if existing_student:
                # Update the existing student's details
                existing_student.sname = sname
                existing_student.save()
            else:
                # Check if the user has already added the maximum number of students
                max_students = 10 # set the maximum number of students here
                num_students = AddStudent.objects.filter(user2=user1).count()
                if num_students >= max_students:
                    return HttpResponse("You have already added the maximum number of students.")
                
                # Create a new AddStudent object
                add = AddStudent(user2=user1, sname=sname, studentid=studentid)
                add.save()

        Student = AddStudent.objects.filter(user2=user1)
        return render(request, 'addstudent.html', {'Student': Student})
    return redirect('/')
"""

def viewissuedbook(request):
    issuedbooks = IssueBook.objects.all()
    lis = []
    for books in issuedbooks:
        issdate = str(books.issuedate.day) + '-' + str(books.issuedate.month) + '-' + str(books.issuedate.year)
        expdate = str(books.expirydate.day) + '-' + str(books.expirydate.month) + '-' + str(books.expirydate.year)
        
        # Exclude teachers from fine calculation
        try:
            student = User.objects.get(username=books.studentid)
            if student.is_teacher:
                fine = "No Fine"
            else:
                # Calculate fine for students
                days = (date.today() - books.issuedate).days
                fine = max(0, days - 15) * 10  # Calculate fine, capped at 0 if negative

            book = AddBook.objects.get(bookid=books.book1)

            t = (student.first_name + " " + student.last_name, student.username, book.bookname, book.sem, book.subject, issdate, expdate, fine)
            lis.append(t)
        except (AddBook.DoesNotExist, User.DoesNotExist):
            pass

    return render(request, 'viewissuedbook.html', {'lis': lis})








def bookreserve(request):
    books = AddBook.objects.filter(category="Not-Issued")
    book_list = []
    for book in books:
        book_name = book.bookname
        book_id = book.bookid
        sem = book.sem
        subject = book.subject
        book_list.append({'name': book_name, 'ID': book_id,'sem': sem, 'subject': subject})
    return render(request, 'bookreserve.html', {'books': book_list})


def r_Search(request):
    query2 = request.GET.get("query2")
    sem = request.GET.get("query2")
    subject = request.GET.get("query2")
    
    Book = AddBook.objects.filter(Q(bookname__icontains=query2) | Q(sem__icontains=query2) | Q(subject__icontains=query2))
    
    book_list = []
    for book in Book:
        book_name = book.bookname
        book_id = book.bookid
        sem = book.sem
        subject = book.subject
        category = book.category
        book_list.append({'bookname': book_name, 'bookid' : book_id, 'sem': sem, 'subject': subject, 'category' : category})
    
    
    params1 = {'Book': book_list, 'query': query2}
    return render(request, 'student.html', params1)



def r1_Search(request):
    query2 = request.GET.get("query2")
    sem = request.GET.get("query2")
    subject = request.GET.get("query2")
    
    Book = AddBook.objects.filter(Q(bookname__icontains=query2) | Q(sem__icontains=query2) | Q(subject__icontains=query2))
    
    book_list = []
    for book in Book:
        book_name = book.bookname
        book_id = book.bookid
        sem = book.sem
        subject = book.subject
        category = book.category
        book_list.append({'bookname': book_name, 'bookid' : book_id, 'sem': sem, 'subject': subject, 'category' : category})
    
    
    params1 = {'Book': book_list, 'query': query2}
    return render(request, 'teacher.html', params1)



@login_required
def reservebooksubmission(request):
    if request.method == 'POST':
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            #us= User.username
            user1 = User.objects.get(id=user_id)
            studentid = request.POST['studentid']
            book1 = request.POST['book1']
            store = AddBook.objects.filter(bookid=book1)
            
            # Update the Brequest cell with the username of the currently logged-in user
            store.update(is_reserved=studentid)

            def get_category(addbook):
                if addbook.category == "Not-Issued":
                    addbook.category = "To-be-Reserved"
                    addbook.Rrequest = "0"
                    obj = ReservedBook(user2=user1, studentid=studentid, book1=book1)
                    obj.save()
                    addbook.save()
                    # Send request to admin
                    admin_email = "arjunkumar20021228@gmail.com"  # Replace with the admin's email address
                    subject = "Book Reserving Request"
                    message = f"User ID: {user_id}\nBook ID: {book1}"
                    send_mail(subject, message, user1.email, [admin_email], fail_silently=False)
                else:
                    messages.error(request, "Book already issued !!!")

            category_list = list(set(map(get_category, store)))
            Issue = ReservedBook.objects.all()
            return render(request, 'viewreservedbooks.html', {'Issue': Issue})
        else:
            messages.error(request, "User ID not found in session.")
            return redirect('/viewreservedbooks')
    return redirect('/viewreservedbooks')
    
"""def book_detail(request, book_id):
    book = get_object_or_404(AddBook, pk=book_id)

    if request.method == 'POST':
        if 'reserve_button' in request.POST:
            book.reserve_book()

    return render(request, 'book_detail.html', {'book': book})"""

@login_required
def viewreservedbooks(request):
    issuedbooks = ReservedBook.objects.filter(studentid=request.user)
    lis = []
    for books in issuedbooks:
        issdate = str(books.issuedate.day) + '-' + str(books.issuedate.month) + '-' + str(books.issuedate.year)
        expdate = str(books.expirydate.day) + '-' + str(books.expirydate.month) + '-' + str(books.expirydate.year)
        # fine calculation
        days = (date.today() - books.issuedate).days
        fine = max(0, days - 15) *10  # Calculate fine, capped at 0 if negative

        try:
            book = AddBook.objects.get(bookid=books.book1)
            student = request.user

            t = (student.first_name+" "+student.last_name, student.username, book.bookname, book.sem, book.subject)
            lis.append(t)
        except (AddBook.DoesNotExist):
            pass

    return render(request, 'viewreservedbooks.html', {'lis': lis})




from django.core.mail import send_mail

@login_required
def borrowbooksubmission(request):
    if request.method == 'POST':
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            studentid = request.POST['studentid']
            book1 = request.POST['book1']
            store = AddBook.objects.filter(bookid=book1)
            
            # Update the Brequest cell with the username of the currently logged-in user
            store.update(Brequest=studentid)

            def get_category(addbook):
                if addbook.category == "Not-Issued":
                    addbook.category = "To-be-Issued"
                    addbook.Rrequest = "0"
                    obj = BorrowBook(user2=user1, studentid=studentid, book1=book1)
                    obj.save()
                    addbook.save()
                    # Send request to admin
                    admin_email = "arjunkumar20021228@gmail.com"  # Replace with the admin's email address
                    subject = "Book Borrowing Request"
                    message = f"User ID: {user_id}\nBook ID: {book1}"
                    send_mail(subject, message, user1.email, [admin_email], fail_silently=False)
                else:
                    messages.error(request, "Book already issued !!!")

            category_list = list(set(map(get_category, store)))
            Issue = BorrowBook.objects.all()
            return render(request, 'logout.html', {'Issue': Issue})
        else:
            messages.error(request, "User ID not found in session.")
            return redirect('/logout')
    return redirect('/logout')



@login_required
def s_borrowhistory(request):
    issuedbooks = BorrowBook.objects.filter(studentid=request.user)
    lis = []
    for books in issuedbooks:
        issdate = str(books.issuedate.day) + '-' + str(books.issuedate.month) + '-' + str(books.issuedate.year)
        expdate = str(books.expirydate.day) + '-' + str(books.expirydate.month) + '-' + str(books.expirydate.year)
        # fine calculation
        days = (date.today() - books.issuedate).days
        fine = max(0, days - 15) * 10  # Calculate fine, capped at 0 if negative

        try:
            book = AddBook.objects.get(bookid=books.book1)
            student = request.user

            t = (student.first_name + " " + student.last_name, student.username, book.bookname, book.sem, book.subject)
            lis.append(t)
        except AddBook.DoesNotExist:
            pass

    return render(request, 's_borrowhistory.html', {'lis': lis})



"""
def bookrenewalsubmission(request):
    if request.method == 'POST':
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            studentid = request.POST['studentid']
            book1 = request.POST['book1']
            store = AddBook.objects.filter(bookid=book1)
            
            # Update the Brequest cell with the username of the currently logged-in user
            store.update(Rrequest=studentid)

            def get_category(addbook):
                if addbook.category == "Not-Issued":
                    addbook.category = "To-be-Issued"
                    obj = RenewBook(user2=user1, studentid=studentid, book1=book1)
                    obj.save()
                    addbook.save()
                    # Send request to admin
                    admin_email = "arjunkumar20021228@gmail.com"  # Replace with the admin's email address
                    subject = "Book Renewal Request"
                    message = f"User ID: {user_id}\nBook ID: {book1}"
                    send_mail(subject, message, user1.email, [admin_email], fail_silently=False)
                else:
                    messages.error(request, "Book already issued !!!")

            category_list = list(set(map(get_category, store)))
            Issue = RenewBook.objects.all()
            return render(request, 'bookrenewal.html', {'Issue': Issue})
        else:
            messages.error(request, "User ID not found in session.")
            return redirect('/')
    return redirect('/')
"""




def deleteuser(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('viewstudents')
    


@login_required
def viewtablebooked(request):
    timeslots = TimeSlot.objects.all()
    return render(request, 'viewtablebooked.html', {'timeslots': timeslots})


@login_required
def book_slot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            # Process the form data and save the time slot
            # Example code:
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            TimeSlot.objects.create(user=request.user, start_time=start_time, end_time=end_time)
            return redirect('book_slot')
    else:
        form = TimeSlotForm()
    return render(request, 'book_slot.html', {'form': form})






@login_required
def book_review(request):
    book_id = request.GET.get('book_id')
    return render(request, 'book_review.html', {'book_id': book_id})

@login_required
def submit_review(request):
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        review_text = request.POST.get('review_text')
        if book_name:
            try:
                review = Review(user=request.user, book_name=book_name, review_text=review_text)
                review.save()
                return redirect('review_history')
            except ValueError:
                return HttpResponseBadRequest("Invalid book name")
    return HttpResponseBadRequest("Invalid request")

@login_required
def review_history(request):
    user_reviews = Review.objects.filter(user=request.user)
    return render(request, 'review_history.html', {'reviews': user_reviews})





def s_fine(request):
    issuedbooks = IssueBook.objects.filter(studentid=request.user)
    lis = []
    for books in issuedbooks:
        issdate = str(books.issuedate.day) + '-' + str(books.issuedate.month) + '-' + str(books.issuedate.year)
        expdate = str(books.expirydate.day) + '-' + str(books.expirydate.month) + '-' + str(books.expirydate.year)
        # fine calculation
        days = (date.today() - books.issuedate).days
        fine = max(0, days - 15) *10  # Calculate fine, capped at 0 if negative

        try:
            book = AddBook.objects.get(bookid=books.book1)
            student = User.objects.get(username=books.studentid)

            t = (student.first_name+" "+student.last_name, student.username, book.bookname,book.sem, book.subject, issdate, expdate, fine)
            lis.append(t)
        except (AddBook.DoesNotExist, User.DoesNotExist):
            pass

    return render(request, 'viewissuedbook.html', {'lis': lis})
    return render(request, 's_fine.html')