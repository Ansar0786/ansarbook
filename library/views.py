from django.shortcuts import render, get_object_or_404, redirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import BookForm
from .models import Book


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):
    form1=forms.StudentUserForm()

    mydict={'form1':form1}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)

        if form1.is_valid() :
            user=form1.save()
            user.set_password(user.password)
            user.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def viewbook_view(request):
#     books=models.Book.objects.all()
#     data = {}
#     data['object_list'] = books
#     return render(request,'library/book_list.html',data)

def book_list(request):
    book = Book.objects.all()
    data = {}
    data['object_list'] = book
    return render(request, 'library/book_list.html', data)


#update book r
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def book_update(request, pk, template_name='library/book_form.html'):
    book= get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, template_name, {'form':form})



def book_delete(request, pk,):
    book= get_object_or_404(Book, pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'object':book})


def allbook(request):
    books = Book.objects.all()
    data = {}
    data['object_list']= books
    return render(request,'library/allbook.html',data)

#here end








