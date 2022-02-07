from django import forms

class SignupForm(forms.Form):
    sFirstName = forms.CharField(max_length=100,strip=True,required=True,
                        error_messages={'required': 'First Name can"t be empty'})
    sLastName = forms.CharField(max_length=100,strip=True,required=True,
                        error_messages={'required': 'Last Name can"t be empty'})
    sUsername = forms.CharField(max_length=100,strip=True,required=True,
                        error_messages={'required': 'Username is Required'})
    sEmail = forms.EmailField(max_length=50)

    """
    PASSWORD REQUIREMENTS

    min len - 6
    a special char '[^a-zA-Z0-9]'
    both upper and lower case 

    """
    sPassword = forms.CharField(max_length=15,min_length=6,strip=True,
                        error_messages={'required': 'Password is Required'})
    sConfirmPassword = forms.CharField(max_length=50,min_length=6,strip=True,
                        error_messages={'required': 'Password Confirmatoin is important'})
    
    # sPassword = forms.RegexField(min_length=6,regex=".*[A-Z]*[a-z]*[^a-zA-Z0-9]")

class LoginForm(forms.Form):
    sUsername = forms.CharField(max_length=100,strip=True,required=True,
                        error_messages={'required': 'Username is Required to login'})
    sPassword = forms.CharField(max_length=50,min_length=6,strip=True,
                        error_messages={'required': 'Password is Required to login'})