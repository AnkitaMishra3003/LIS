from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer
from .models import User
from .models import Transaction
from .serializers import TransactionSerializer
from .serializers import UserSerializer
import datetime
from datetime import date
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User as auth_user
from .models import Req
from .serializers import ReqSerializer
from collections import Counter

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes=[
        '/token',
        '/token/refresh',
    ]
    return Response(routes)

@api_view(['GET'])
def getBooks(request):
    books=Book.objects.all()
    bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)

@api_view(['GET'])
def getlatestBooks(request):
    last_ten=Book.objects.all().order_by('-id')[:10]
    bookSerializer=BookSerializer(last_ten, many=True)
    return Response(bookSerializer.data)

@api_view(['GET'])
def getBook(request, pk):
    book = Book.objects.get(id = pk)
    bookSerializer = BookSerializer(book, many=False)
    return Response(bookSerializer.data)

@api_view(['GET'])
def getBookISBN(request, pk):
    book = Book.objects.get(ISBN = pk)
    bookSerializer = BookSerializer(book, many=False)
    return Response(bookSerializer.data)

@api_view(['GET'])
def getQuery(request, search):
    # print(search)
    books=Book.objects.all()
    if search is not None:
        books=books.filter(title__icontains=search)
        bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)
@api_view(['GET'])
def getTitAvailable(request, search):
    books=Book.objects.all()
    if search is not None:
        books=books.filter(title__icontains=search, available=True, reserved=False)
        bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)
@api_view(['GET'])
def getTitReserve(request, search):
    books=Book.objects.all()
    if search is not None:
        books=books.filter(title__icontains=search, available=False, reserved=True)
        bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)
@api_view(['GET'])
def getCategory(request, pk):
    # book = Book.objects.get(category = pk)
    # bookSerializer = BookSerializer(book, many=False)
    # return Response(bookSerializer.data)
    books=Book.objects.all()
    if pk is not None:
        books=books.filter(category=pk)
        bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)
@api_view(['GET'])
def getAuthor(request, search):
    # print(search)
    books=Book.objects.all()
    if search is not None:
        books=books.filter(author__icontains=search)
        bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)
@api_view(['GET'])
def getUsers(request):
    users=User.objects.all()
    userSerializer=UserSerializer(users, many=True)
    return Response(userSerializer.data)
@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id = pk)
    userSerializer = UserSerializer(user, many=False)
    return Response(userSerializer.data)
@api_view(['GET'])
def getUserCode(request, ucode):
    users = User.objects.all()
    if ucode is not None:
        users=users.filter(code__icontains=ucode)
        userSerializer=UserSerializer(users, many=True)
    return Response(userSerializer.data)

@api_view(['GET'])
def login(request, usern, passwd):
    users=User.objects.all()
    if usern is not None:
        users=users.filter(username=usern)
        if passwd is not None:
            users=users.filter(password=passwd)
            userSerializer=UserSerializer(users, many=True)
    return Response(userSerializer.data)
@api_view(['POST'])
def addBook(request):
    data=request.data
    bookSerializer=BookSerializer(data=data)
    if bookSerializer.is_valid():
        
        bookSerializer.save()
    return Response(bookSerializer.data)

@api_view(['GET', 'POST'])
def genISBN(request):
    
    books=Book.objects.all()
    for book in books:
        position=book.id%10
        rack=(book.id//10)%5
        cupboard=book.id//50
        isbn=cupboard*100+rack*10+position
        book.ISBN=isbn
        book.cupboard=cupboard
        book.rack = rack
        book.position=position
        book.save()
    bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)

@api_view(['GET', 'POST'])
def genISBNsingle(request):
    
    book=Book.objects.all().latest('id')
   
    position=book.id%10
    rack=(book.id//10)%5
    cupboard=book.id//50
    isbn=cupboard*100+rack*10+position
    book.ISBN=isbn
    book.cupboard=cupboard
    book.rack = rack
    book.position=position
    book.save()
    bookSerializer=BookSerializer(book, many=False)
    return Response(bookSerializer.data)

@api_view(['DELETE'])
def deleteBook(request, pk):
    book=Book.objects.get(id=pk)
    if (book.available==False or book.reserved==True):
        return Response('Book is not available to delete')
    book.delete()
    return Response('Book was deleted')

@api_view(['GET', 'POST'])
def register(request):
    data = request.data
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        # Create a new user
        auth_user.objects.create_user(
            username=data['code'],
            email=data['email'],
            password=data['password']  # You may want to hash the password properly
        )

        # Save the user details provided during registration
        user_serializer.save()

        return Response(user_serializer.data)
    else:
        return Response(user_serializer.errors)

@api_view(['GET','POST'])
def getMaxBooks(request):
    
    user=User.objects.latest("id")
    if user.type == 1:
        user.max_books = 2
    if user.type == 2:
        user.max_books = 4
    if user.type == 3:
        user.max_books = 6
    if user.type == 4:
        user.max_books = 10
    user.save()
    return Response(user.max_books)
@api_view(['POST'])
def edituser(request, pk):
    data=request.data
    user=User.objects.get(id=pk)
    userSerializer=UserSerializer(instance=user, data=data)
    if userSerializer.is_valid():
        userSerializer.save()
    return Response(userSerializer.data)
@api_view(['POST'])
def editbook(request, pk):
    data=request.data
    book=Book.objects.get(id=pk)
    bookSerializer=BookSerializer(instance=book, data=data)
    if bookSerializer.is_valid():
        bookSerializer.save()
    return Response(bookSerializer.data)
@api_view(['DELETE'])
def deleteuser(request, pk):
    user=User.objects.get(id=pk)
    u = auth_user.objects.get(username=user.code)
    u.delete()
    user.delete()
    return Response('User was deleted')
@api_view(['GET','POST'])
#issued_code : add
def issue(request, pk1, pk2):
    book=Book.objects.get(id=pk1)
    user=User.objects.get(id=pk2)
    if (book.available==True):
        if (book.reserved==False):
            if (user.active_no+user.reserve_no<user.max_books):
                user.active_no=user.active_no+1
                book.available=False
                book.issued_code=user.code
                user.active_books.add(book)
                user.save()
                book.save()
                issue_dates=date.today()
                if user.type==1:
                    MONTHS=1
                elif user.type==2:
                    MONTHS=1
                elif user.type==3:
                    MONTHS=3
                elif user.type==4:
                    MONTHS=6
                due_dates=issue_dates+relativedelta(months=MONTHS)
                trans=Transaction(category=1, issue_date=issue_dates, due_date=due_dates, user_code=user.code, book_id=book.ISBN, active=True)
                transSerializer=TransactionSerializer(trans, many=False)
                trans.save()
                user.transactions.add(trans)
                user.save()
                return Response(transSerializer.data)
    if (book.available==True):
        if(book.reserved==True):
            if (user.reserved_books.contains(book)):
                if(date.today()<=book.max_reserve_date):
                    user.active_no=user.active_no+1
                    user.reserve_no=user.reserve_no-1
                    book.reserved=False
                    book.available=False
                    book.issued_code=user.code
                    book.reserved_code='0'
                    user.reserved_books.remove(book)
                    user.active_books.add(book)
                    issue_dates=date.today()
                    if user.type==1:
                        MONTHS=1
                    elif user.type==2:
                        MONTHS=1
                    elif user.type==3:
                        MONTHS=3
                    elif user.type==4:
                        MONTHS=6
                    due_dates=issue_dates+relativedelta(months=MONTHS)
                    trans=Transaction(category=1, issue_date=issue_dates, due_date=due_dates, user_code=user.code, book_id=book.ISBN, active=True)
                    transSerializer=TransactionSerializer(trans, many=False)
                    trans.save()
                    user.transactions.add(trans)
                    user.save()
                    book.save()
                    return Response(transSerializer.data)
    return Response(book.available)
@api_view(['GET'])
def getTransaction(request, pk):
    trans=Transaction.objects.get(id=pk)
    transSerializer=TransactionSerializer(trans, many=False)
    return Response(transSerializer.data)
#crossed the due date and didnt return book yet
@api_view(['GET', 'POST'])
def cross(request):
    current=date.today()
    trans=Transaction.objects.filter(due_date__lt=current, category = 1)
    users=User.objects.all()
    for user in users:
        for tran in trans:
            if (user.code==tran.user_code):
                user.fine=(current-tran.due_date).days*20
                tran.dues=user.fine
                user.notification='You have pending books to return!! The book ISBN is: {}, Present fine is: {}'.format(tran.book_id, user.fine)
                user.save()
    trans=Transaction.objects.filter(category=3, max_date_of_reserve__lt=current)
    for tran in trans:
        book=Book.objects.get(ISBN=tran.book_id)
        book.reserved=False
        book.available=True
        book.save()
    for user in users:
        for tran in trans:
            if (user.code==tran.user_code):
                user.notification='The book {} is no longer reserved for you!!'.format(tran.book_id)
                book1=Book.objects.get(ISBN=tran.book_id)
                user.reserved_books.remove(book1)
                book1.max_reserve_date=date.today()+relativedelta(years=5)
                user.save()
                user.reserve_no=user.reserved_books.count()
                user.save()
                book1.issued_code='0'
                book1.save()
    # userfilter=User.objects.filter(fine__gt=0)
    # userSerializer=UserSerializer(userfilter, many=True)
    transfilter = Transaction.objects.filter(dues__gt=0, category = 1)
    transSerializer = TransactionSerializer(transfilter, many=True)
    return Response(transSerializer.data)


@api_view(['GET', 'POST'])
def returnbook(request, pk1, pk2):
    try:
        book = Book.objects.get(id=pk1)
        user = User.objects.get(id=pk2)

        if not book.available:
            if book in user.active_books.all():  # Checking if the book is in active_books
                user.active_no -= 1
                user.active_books.remove(book)
                book.available = True
                book.issued_code = '0'
                book.save()  # Saving book changes
                user.save()  # Saving user changes

                return_dates = date.today()
                # tranissue = Transaction.objects.filter(active=True, user_code=user.code, book_id=book.ISBN, category=1)
                print(user.transactions.all())
                tranissue = user.transactions.filter(book_id=book.ISBN, category=1).latest('id')
                tranissue.dues = 0
                user.fine = 0
                # tranissue = tranissue.objects.latest('id')
                due = (return_dates - tranissue.due_date).days * 20
                if due < 0:
                    due = 0
                tranret = Transaction(category=2, return_date=return_dates, dues=due, user_code=user.code, book_id=book.ISBN, issue_date=tranissue.issue_date)
                tranret.save()
                user.transactions.add(tranret)
                user.save()

                if book.reserved:
                    book.available = True
                    max_date = return_dates + relativedelta(days=7)
                    tranres = Transaction.objects.filter(category=3, book_id=book.ISBN).latest('id')
                    tranres.max_date_of_reserve = max_date
                    book.max_reserve_date=max_date
                    book.save()
                    tranres.save()

                return Response(book.available)
            else:
                return Response("Book is not issued to this user.")
        else:
            return Response("Book is already available.")
    except Book.DoesNotExist:
        return Response("Book does not exist.")
    except User.DoesNotExist:
        return Response("User does not exist.")




@api_view(['GET', 'POST'])
def reservebook(request, pk1, pk2):
    book=Book.objects.get(id=pk1)
    user=User.objects.get(id=pk2)
    if (book.available==False):
        if (book.reserved==False):
            if (user.active_no+user.reserve_no<user.max_books and user.code!=book.issued_code):
                # user.reserve_no=user.reserve_no+1
                user.reserved_books.add(book)
                user.save()
                user.reserve_no=user.reserved_books.count()
                book.available=False
                book.reserved=True
                book.reserved_code=user.code
                trans=Transaction(category=3, user_code=user.code, book_id=book.ISBN, issue_date=date.today(), max_date_of_reserve=user.valid_till)
                trans.save()
                user.transactions.add(trans)
                book.save()
                user.save()
    return Response(book.available)

@api_view(['GET'])
def getLatestTransaction(request):
    trans = Transaction.objects.latest('id')
    transSerializer = TransactionSerializer(trans, many=False)
    return Response(transSerializer.data)

@api_view(['GET'])
def customTrans(request, isbn, uid, cat):
    trans=Transaction.objects.filter(book_id=isbn, user_code=uid, category=cat).latest('id')
    transSerializer = TransactionSerializer(trans, many=False)
    return Response(transSerializer.data)
@api_view(['GET'])
def getUserTransactions(request, code):
    trans = Transaction.objects.all().filter(user_code=code).order_by('-id')
    transSerializer = TransactionSerializer(trans, many=True)
    return Response(transSerializer.data)
@api_view(['GET'])
def getAllTransactions(request):
    trans = Transaction.objects.all().order_by('-id')
    transSerializer = TransactionSerializer(trans, many=True)
    return Response(transSerializer.data)

@api_view(['GET', 'POST'])
def takeprocreq(request, pk, tit, auth, link):
    # data=request.data
    r=Req(ucode=User.objects.get(id=pk).code, bname=tit, bauthor=auth, blink=link, request=1)
    r.save()
    return Response(r.bname)
@api_view(['GET', 'POST'])
def notinshelf(request, pk, isbn):
    r=Req(ucode=User.objects.get(id=pk).code, bISBN=isbn, bname=Book.objects.get(ISBN=isbn).title, bauthor=Book.objects.get(ISBN=isbn).author, request=2)
    r.save()
    return Response(r.ucode)

@api_view(['GET', 'POST'])
def makedb(request):
    all_books=Book.objects.all()
    for book in all_books:
        book.delete()
    for i in range(0, 10):
        b=Book(title='Switching and Finite Automata Theory', author='Zvi Kohavi', publisher='Cambridge', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Let us C', author='Byron Gottfried', publisher='Tata McGraw-Hill', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Automata and Computability', author='Dexter Kozen', publisher='Springer', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Software Engineering at Google', author='Titus, Manshreck and Wright', publisher='O Reilly', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='An Introduction to GCC', author='Brian Gough', publisher='Network Theory Ltd.', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Algorithm Design', author='Kleinberg and Tardos', publisher='Pearson', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Compilers - Principles, Techniques and Tools', author='Aho, Sethi and Ullman', publisher='Addison-Wesley', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Machine Learning', author='Tom Mitchell', publisher='McGraw Hill', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Operating Systems Concepts', author='A. Silverschatz, Galvin and Gagne', publisher='Wiley', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Mastering Blockchain', author='Imran Bashir', publisher='Packt Publishing', available=True, reserved=False, category=9)
        b.save()
    for i in range(0, 10):
        b=Book(title='Strength of Materials', author='R.K. Bansal', publisher='Laxmi Publications', available=True, reserved=False, category=23)
        b.save()
    for i in range(0, 10):
        b=Book(title='Surveying: Theory and Practice', author='B.C. Punmia', publisher='Laxmi Publications', available=True, reserved=False, category=23)
        b.save()
    for i in range(0, 10):
        b=Book(title='Fluid Mechanics', author='Cengel and Cimbala', publisher='McGraw-Hill', available=True, reserved=False, category=23)
        b.save()
    for i in range(0, 10):
        b=Book(title='Design of Reinforced Concrete Structures', author='N. Subramanian', publisher='Oxford University Press', available=True, reserved=False, category=23)
        b.save()
    books=Book.objects.all()
    bookSerializer=BookSerializer(books, many=True)
    return Response(bookSerializer.data)

@api_view(['GET', 'POST'])
def autosuggest(request, pk):
    user=User.objects.get(id=pk)
    dep=user.dept
    if (user.count<5):
        if dep=='CS':
            rel=9
        elif dep=='EE':
            rel=12
        elif dep=='MA':
            rel=8
        elif dep=='EC':
            rel=12
        elif dep=='ME':
            rel=11
        elif dep=='CH':
            rel=15
        elif dep=='CE':
            rel=23
        elif dep=='CY':
            rel=14
        elif dep=='PH':
            rel=13
        elif dep=='EX':
            rel=16
        elif dep=='GG':
            rel=16
        elif dep=='NA':
            rel=17
        elif dep=='MT':
            rel=18
        elif dep=='BS':
            rel=19
        elif dep=='AR':
            rel=20
        elif dep=='AG':
            rel=21
        elif dep=='MI':
            rel=22
        books=Book.objects.filter(category=rel, available=True, reserved=False)
    else:
        cat_counter = Counter(user.cat)
        most_common_cat, frequency = cat_counter.most_common(1)[0]
        books=Book.objects.filter(category=most_common_cat, available=True, reserved=False)
        
    name=[]
    mybooks = []
    for book in books:
        if ((book.title in name)==False):
            name.append(book.title)
            mybooks.append(book)
    i = min(8, len(mybooks))
    mybooks = mybooks[:i]
    bookSerializer=BookSerializer(mybooks, many=True)
    return Response(bookSerializer.data)