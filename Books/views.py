from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,reverse
from .models import Book,Tags,SharedWithMe #,OpenTimings
from .helper import saveFirstPage,getBookTitle
from django.conf import settings
from django.http import HttpResponse,FileResponse
from .forms import AddBookForm
from reportlab.pdfgen import canvas
from django.db.models import Min,Max,Sum
from collections import OrderedDict

from django.contrib.auth.models import User

from django.core.files.uploadedfile import TemporaryUploadedFile,InMemoryUploadedFile

import os
import io
import re
import datetime

from io import BytesIO
from zipfile import ZipFile

from . import constant

# from django.views.decorators.cache import cache_page

def shareMultiple(request, books_id, share_to):
    share_to_user = User.objects.get(id=share_to)
    books_alr_shared = []
    for i in SharedWithMe.objects.all():
        print(i.book.name)
    for _id in books_id:
        _book = Book.objects.get(id=_id)
        if SharedWithMe.objects.filter(user__exact=share_to_user, book__exact=_book):
            books_alr_shared.append(_book.name)
            for i in SharedWithMe.objects.filter(user__exact=share_to_user, book__exact=_book):
                print(i.book.name)
        else:
            sh = SharedWithMe(user=share_to_user, book=_book, shared_by=request.user)
            sh.save()

    return HttpResponse(', '.join(books_alr_shared) + "books are already shared" if books_alr_shared else "Books Shared Successfully")


def handleMultipleBooks(request, _action):
    if _action == 'share':
        books = str(request.body)
        books = books[2: len(books)-1].split('/')
        return shareMultiple(request, books, 2)
    
    return HttpResponse("Success")


def pageNotExist(request):
    return render(request, 'page_not_exist.html')
    

def getSelectedBooks(request,base_url):
    path = request.path
    path = path[path.find(base_url)+len(base_url):-1]
    path = os.path.join(path)

    selected_books = []

    if '/' in path:
        selected_books = path.split('/')
    elif '\\' in path:
        selected_books = path.split('\\')
    else:
        selected_books.append(path)

    return selected_books


def getFullPath(book_id):
    book_path = os.path.join(str(settings.MEDIA_ROOT),str(Book.objects.get(id=book_id).pdf))
    return book_path

@login_required
def downloadMultiple(request,*books_id):

    base_url = 'download-multiple-books/'
    books_to_download = getSelectedBooks(request,base_url)

    # create zip and write data in it 
    file_in_memory = BytesIO()        # file object created in memory (not in disk)
    zip = ZipFile(file_in_memory, "w")

    for _id in books_to_download:
        book_path = getFullPath(_id)
        zip.write(book_path,f'Your_books/{Book.objects.get(id=_id).name}.pdf')
    
    zip.close()

    # create response 
    response = HttpResponse(content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="bookshelf_books.zip"'

    file_in_memory.seek(0)
    response.write(file_in_memory.read())

    return response

@login_required
def deleteBook(request,id):
    bk_path = getFullPath(id)
    temp = bk_path.replace(constant.PDF_FOLDER_NAME, constant.IMAGE_FOLDER_NAME, 1)
    img_path = temp.replace(constant.PDF_EXTENSION, constant.IMAGE_EXTENSION, 1)

    if os.path.exists(bk_path):
        os.remove(bk_path)
    if os.path.exists(img_path):
        os.remove(img_path)

    book = Book.objects.get(id=id).delete()

    return redirect('home')


@login_required
def deleteMultiple(request,*books_id):
    base_url = 'delete-multiple-books/'
    books_to_delete = getSelectedBooks(request,base_url)
        
    for _id in books_to_delete:
        deleteBook(request,_id)

    return redirect('home')



@login_required
def pdfClosed(request):
    url = request.POST['sBookUrl']
    pdf = url[url.find("pdf"):]
    pdf_url = re.sub(r"/$",".pdf",pdf)
    
    current_book = Book.objects.get(pdf=pdf_url)
    
    closed_time = datetime.datetime.now()
    current_book.close_time = closed_time
    current_book.save()

    current_book = Book.objects.get(pdf=pdf_url)
    viewed_seconds = int((current_book.close_time - current_book.open_time).total_seconds())
    current_book.viewed_time += viewed_seconds
    current_book.save()

    return HttpResponse("DATA ACCEPTED")

# @cache_page(30)
@login_required
def showPdf(request,id):
    path_with_ext = os.path.join(constant.PDF_FOLDER_NAME, str(id) + ".pdf")

    filepath = os.path.join('media', path_with_ext)

    dt = datetime.datetime.now()

    current_book = None

    _qSet = Book.objects.filter(id=id,user__exact=request.user)
    if _qSet.exists():
        current_book = _qSet.first()
    else:
        return render(request, 'book_not_available.html')

    current_book.open_time = dt
    current_book.save()

    # return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    
    context = {
        'pdf_path': filepath
    }

    return render(request,'pdf_reader.html',context)



def getTagRows(request,tag):
    tags = Tags.objects.all().filter(book__user__exact = request.user,tag=tag)
    return tags

def getRows(request, _category):
    result = None
    if _category == constant.RECENT_BOOKS:
        result = Book.objects.filter(user__exact=request.user,open_time__isnull=False).order_by('-open_time')[0:10]
    elif _category == constant.FAV_BOOKS:
        result = Book.objects.filter(user__exact=request.user,viewed_time__gt = 0).order_by('-viewed_time')[0:6]
    else:
        tags = Tags.objects.all().filter(book__user__exact = request.user,tag=_category)
        result = [item.book for item in tags]
    
    return result

@login_required
def home(request,_category=None):
    # if book_tag and not Tags.objects.filter(book__user__exact=request.user,tag=book_tag).exists():
    #     return render(request, 'page_not_exist.html')

    if _category is None:
        # send tags as cookies to client 
        tag_names = list(Tags.objects.filter(book__user__exact=request.user).values_list('tag',flat=True).distinct())
        response = render(request, 'home.html', {})
        response.set_cookie('tags',tag_names)


    else:
        # send row acc. to category 
        _row = getRows(request, _category)
        if not _row:
            return render(request, 'no_books_found.html')

        books_dict = OrderedDict()
        books_dict[_category] = _row
        
        # carousel items arrangement
        for tag,item in books_dict.items():
            if type(item[0]) != list:
                item_list = []
                tmp = []
                for i in range(len(item)):
                    tmp.append(item[i])
                    if (i+1) % 5 == 0 or i == len(item)-1:
                        item_list.append(tmp)
                        tmp = []

                books_dict[tag] = item_list

        context = {
            'books_dict': books_dict
        }

        response = render(request, 'books_row.html', context)

    return response

# -------------------------------------
    
    # books_dict = OrderedDict()

    # if book_tag is None:
    #     # Get all recent books
    #     recent_books = Book.objects.filter(user__exact=request.user,open_time__isnull=False).order_by('-open_time')[0:10]

    #     # Get all Fav books
    #     fav_books = Book.objects.filter(user__exact=request.user,viewed_time__gt = 0).order_by('-viewed_time')[0:6]

    #     if recent_books:
    #         books_dict['recent_books'] = recent_books
    #     if fav_books:
    #         books_dict['fav_books'] = fav_books
    # else:
    #     tags = getTagRows(request,book_tag)
    #     books_dict[book_tag] = [item.book for item in tags]

    # _template = None
    # tag_names = None

    # if book_tag is None:
    #     # Get all tag names
    #     tag_names = list(Tags.objects.filter(book__user__exact=request.user).values_list('tag',flat=True).distinct())

    #     # if not books_dict and tag_names:
    #     #     initial_tags = tag_names[0:2 if len(tag_names) >=2 else 1]
    #     #     tag_names = tag_names[2:] if len(tag_names) > 2 else []
    #     #     for _tag in initial_tags:
    #     #         tags = getTagRows(request,_tag)
    #     #         books_dict[_tag] = [item.book for item in tags]
        
    #     return render(request, 'home.html', context)
    #     # _template = 'home.html'

    # else:

    #     _template = 'books_row.html'

    # # carousel items arrangement
    # for tag,item in books_dict.items():
    #     if type(item[0]) != list:
    #         item_list = []
    #         tmp = []
    #         for i in range(len(item)):
    #             tmp.append(item[i])
    #             if (i+1) % 5 == 0 or i == len(item)-1:
    #                 item_list.append(tmp)
    #                 tmp = []

    #         books_dict[tag] = item_list

    # context = {
    #     'books_dict': books_dict,
    # }
        
    # response = render(request, _template, context)

    # if book_tag is None:
    #     response.set_cookie('tags',tag_names)
    
    # return response


@login_required
def addBook(request):


    if request.method == "POST":
        
        form = AddBookForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            book_name = data['sName']
            pdf_file = data['sPdf']
            tags = data['sAllTags']

            for _file in request.FILES.getlist('sPdf'):
                if type(_file) == TemporaryUploadedFile:
                    title = getBookTitle(_file.temporary_file_path())
                elif type(_file) == InMemoryUploadedFile:
                    title = getBookTitle(_file)

                # customize book title
                title = str(title)
                if ':' in title:
                    title = title[0:title.index(':')]
                else:
                    words_arr = title.split(" ")
                    words_arr = words_arr[0:4 if len(words_arr) >= 4 else len(words_arr)]

                    title = " ".join(words_arr)

                title = re.sub(r'[^A-Za-z0-9\s]',"",title)

                book = Book(user=request.user,name=title)
                book.save()

                _name = str(book.id)     # + str(book.id) + "_".join(book.name.split(" "))
                _file.name = _name + ".pdf"
                book.pdf = _file
                book.save()

                tagList = tags.split(" ")

                for tag in tagList:
                    if len(tag.strip()) > 0:
                        newTag = Tags(book=book,tag=tag)
                        newTag.save()

                # create and save first page of pdf as image (jpg)
                pdf_file_path = os.path.join(str(settings.MEDIA_ROOT), str(book.pdf))
                img_output_dir = os.path.join(str(settings.MEDIA_ROOT), constant.IMAGE_FOLDER_NAME)
                if not os.path.isdir(img_output_dir):
                    os.mkdir(img_output_dir)
                img_name = _name

                saveFirstPage(pdf_file_path, img_output_dir, img_name)

            return redirect('home')
                
        else:
            return render(request, 'add_book.html', {'form': form})
    else:
        return render(request, 'add_book.html', {})

@login_required
def searchBook(request):
    
    query = request.GET["query"]
    _books_by_name = Book.objects.filter(user__exact=request.user,name__iregex=r".*"  + str(query) + ".*")
    _books_by_tag = Tags.objects.filter(book__user__exact = request.user,tag__iregex=r".*" + str(query) + ".*").values_list('book',flat=True)
    _books_by_tag = [Book.objects.get(id=id) for id in list(_books_by_tag)]

    books = set()
    for item in _books_by_tag:
        books.add(item)
    for item in _books_by_name:
        books.add(item)
        
    return render(request, 'searchedBooks.html',{'query': query,'books': books})

# _name = str(book.id) + "_" + str(book.name).replace(" ","_")
                # folder_name = 'pdfFirstPageImg'
                # outputDir = os.path.join(str(settings.MEDIA_ROOT),folder_name)
                # if not os.path.isdir(outputDir):
                #     os.mkdir(outputDir)
                # getFirstPage(os.path.join(str(settings.MEDIA_ROOT),str(book.pdf)),outputDir,_name)

            # tagList = tags.split(" ")


            # book = Book(user=request.user,name=book_name)
            # book.save()

            # pdf_file.name = str(book.id) + "_" + book.name + ".pdf"
            # book.pdf = pdf_file
            # book.save()

            # for tag in tagList:
            #     if len(tag.strip()) > 0:
            #         newTag = Tags(book=book,tag=tag)
            #         newTag.save()
        
            # _name = str(book.id) + "_" + str(book.name).replace(" ","_")
            # folder_name = 'pdfFirstPageImg'
            # outputDir = os.path.join(str(settings.MEDIA_ROOT),folder_name)
            # if not os.path.isdir(outputDir):
            #     os.mkdir(outputDir)
            # getFirstPage(os.path.join(str(settings.MEDIA_ROOT),str(book.pdf)),outputDir,_name)

            