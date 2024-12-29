from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
#from django.forms.widgets import DatePickerInput
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date,timedelta

email_regex=RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',message="Please enter valid Email address.")
string_regex=RegexValidator(regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',message="Some special characters like(~!#^`'$|{}<>*) are not allowed")
digits_validate=RegexValidator(regex=r'^(?:\d{10})$',message='Enter a valid  digit number')


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.EmailInput)
    password=forms.CharField(widget=forms.PasswordInput)
    
class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50)
    email=forms.EmailField()
    firstname=forms.CharField()
    lastname=forms.CharField()
    phone=forms.CharField(max_length=12)
    password=forms.CharField(widget=forms.PasswordInput)
    
class ChangeUserForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old Password'}))
    new_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New Password'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}))
    
    class Meta:
        model=CustomUser
        fields=['old_password','new_password','new_password2']
    
class DateDurationField(forms.Field):
    def to_python(self,value):
        return value
    
    def validate(self,value):
        check_in_date=self.parent.cleaned_data['check_in_date']
        check_out_date=self.parent.cleaned_data['check_out_date']
        if check_in_date and check_out_date:
            duration=(check_out_date-check_in_date).days
            if duration <=0:
                raise ValidationError("Check-out date must be after Check-in date.")

class RoomsForm(forms.Form):
    name=forms.CharField(disabled=False)
    photo=forms.CharField(disabled=False)
    quantity=forms.IntegerField(disabled=False)
    price=forms.CharField(disabled=False,label="Price(Kes)")
    check_in_date=forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}),
                                  label="Check-In Date",initial=date.today())#,widget=DatePickerInput())
    check_out_date=forms.DateField(label="Check-Out Date",initial=date.today()+timedelta(days=2))#,widget=DatePickerInput())
    #duration=DateDurationField(disabled=False)
    total=forms.CharField()
    
    REQUIRED_FIELDS=None

class DishesForm(forms.Form):
    name=forms.CharField()
    photo=forms.CharField()
    quantity=forms.IntegerField()
    price=forms.CharField()
    total=forms.CharField()

#forms for editing table rows in admin panel
class DeleteForm(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    firstname=forms.CharField()
    lastname=forms.CharField()
    phone=forms.CharField(max_length=12)
    password=forms.CharField(widget=forms.PasswordInput)

class EditForm(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    firstname=forms.CharField()
    lastname=forms.CharField()
    phone=forms.CharField(max_length=12)
    #password=forms.CharField(widget=forms.PasswordInput)