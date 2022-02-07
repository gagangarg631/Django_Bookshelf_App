from operator import mod
from pyexpat import model
from statistics import mode
from django.db import models
from django.conf import settings


class Book(models.Model):
    name = models.CharField(verbose_name='Book Name',max_length=100,null=True)
    pdf = models.FileField(verbose_name='Pdf File',upload_to='pdf/',null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET("User Deleted"))
    viewed_time = models.IntegerField(verbose_name='Total_Viewed_Seconds',default=0)
    open_time = models.DateTimeField(verbose_name='Pdf_Open_Time',null=True)
    close_time = models.DateTimeField(verbose_name='Pdf_Close_Time',null=True)

    class Meta:
        verbose_name = "Books"

    def __str__(self):
        return str(self.name)
        
    def getPdfImgUrl(self):
        pdfUrl = str(self.pdf.url)
        temp = pdfUrl.replace('pdf','pdfFirstPageImg',1)
        temp = temp.replace('.pdf','.jpg',1)
        return temp

    def getFileName(self):
        pdfAttr = str(self.pdf)
        temp = pdfAttr.replace(".pdf","",1)
        file_name = temp.replace("pdf/","",1)
        return file_name

    def getPdfUrl(self):
        pdfUrl = str(self.pdf.url)
        temp = pdfUrl.replace('.pdf','',1)
        temp = temp.replace('media','read',1)
        return temp

    def getBookName(self):
        pdfUrl = str(self.pdf.url)
        name = pdfUrl[11:].replace('.pdf','',1)
        return name
        
    def getBookId(self):
        return self.id


class Tags(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    tag = models.CharField(verbose_name='Tag',null=True,max_length=50)

    class Meta:
        verbose_name = "Book Tags"

    def __str__(self):
        return self.tag

class SharedWithMe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name="me")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="shared_by")
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)


class Notifications(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    object_to_count = models.CharField(verbose_name='Object_To_Count', max_length=40)
    counts = models.IntegerField(verbose_name='Counts')


# class OpenTimings(models.Model):
#     date_time = models.DateTimeField(verbose_name='DATE_TIME')
#     book = models.ForeignKey(Book,on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = "Timings"
#         ordering = ["-date_time"]

#     def __str__(self):
#         return str(self.date_time)