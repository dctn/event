from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name","phone_no","college_name","department","interested_event","gender","img","bio"]

        widgets = {
            "name": forms.TextInput(attrs={"class":"input","placeholder":"Enter Your Name:"}),
            "college_name": forms.TextInput(attrs={"class":"input","placeholder":"Enter Your College name:"}),
            "department": forms.TextInput(attrs={"class":"input","placeholder":"Enter Your Department name:"}),
            "phone_no": forms.TextInput(attrs={"class":"grow","placeholder":"Enter Your Phone NO:","type":"number"}),
            "img": forms.ClearableFileInput(attrs={"accept": "image/*"  ,"class":"input","placeholder":"upload your profile pic:","type":"file"}),
            "gender": forms.RadioSelect(attrs={"class":"radio radio-primary",}),
            "bio": forms.Textarea(attrs={"class":"textarea min-h-20 resize-none","placeholder":"Set your bio"}),
            "interested_event": forms.Select(attrs={"class":"select select-bordered w-full max-w-sm"})
        }
