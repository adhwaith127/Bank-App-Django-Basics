from django import forms
from .models import UserModel

class UserForm(forms.Form):
    accountnumber=forms.RegexField(widget=forms.NumberInput(attrs={'placeholder':'Enter 5 digit account number'}),label="Account Number",required=True,regex=r'^\d{5}$',error_messages={'unique':'Account already present','invalid':'Account number must be 5 digits'})
    accountname=forms.RegexField(widget=forms.TextInput(attrs={'placeholder':'Enter your name'}),label="Account Name",max_length=35,required=True,regex=r'^[A-Za-z]{3,15}( [A-Za-z]+)?( [A-Za-z]+)?$',error_messages={'invalid':'Invalid account name(3-15 characters)'})
    accountbalance=forms.RegexField(widget=forms.NumberInput(attrs={'placeholder':'Enter your account balance(up to 2 decimal places)'}),label="Account Balance",required=True,regex=r'^\d{1,15}(\.\d{1,2})?$',error_messages={'invalid':'Invalid account balance(up to 2 decimal places)'})
    password=forms.CharField(label="Password",required=True,widget=forms.PasswordInput,error_messages={'required':'Password is required'})
    confirmpassword=forms.CharField(label="Confirm Password",required=True,widget=forms.PasswordInput,error_messages={'required':'Password is required'})


    def clean(self):
        cleaned_data=super().clean()
        password=self.cleaned_data.get('password')
        confirmpassword=self.cleaned_data.get('confirmpassword')
        if password and confirmpassword and password!=confirmpassword:
            self.add_error('confirmpassword','Passwords do not match')
        accountnumber=self.cleaned_data.get('accountnumber')
        if UserModel.objects.filter(accountnumber=accountnumber).exists():
            self.add_error('accountnumber','Account already present')


