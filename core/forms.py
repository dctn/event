from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import *
from PIL import Image
from io import BytesIO
import sys
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

    def clean_img(self):
        img = self.cleaned_data.get("img")
        print("DEBUG SIZE:", img.size)  # test

        if img:
            # if not img.content_type.startswith("image"):
            #     raise forms.ValidationError("Only image files are allowed.")

            if img.size > 2 * 1024 * 1024:  # 2MB = 2 * 1024 * 1024 bytes
                raise forms.ValidationError("Image file size should not exceed 2MB.")
        return img

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     img = self.cleaned_data.get('img')
    #
    #     if img:
    #         # Open the uploaded image
    #         image = Image.open(img)
    #         image = image.convert('RGB')  # Ensure it's RGB
    #
    #         # Resize (optional): adjust to a max width or height
    #         max_size = (800, 800)
    #         image.thumbnail(max_size)
    #
    #         # Save it to memory
    #         output = BytesIO()
    #         image.save(output, format='JPEG', quality=70)  # Adjust quality to compress
    #         output.seek(0)
    #
    #         # Replace the image file in the instance
    #         instance.img = InMemoryUploadedFile(
    #             output, 'ImageField', f"{img.name.split('.')[0]}.jpg",
    #             'image/jpeg', sys.getsizeof(output), None
    #         )
    #
    #     if commit:
    #         instance.save()
    #
    #     return instance


class EventForm(forms.ModelForm):
    event_starting_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"class": "input", "type": "time"}),
        input_formats=['%H:%M', '%H:%M:%S'],
    )
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ["event_id","is_verified","created_by","current_slots"]

        widgets = {
            "name": forms.TextInput(attrs={"class":"input","placeholder":"John"}),
            "location": forms.TextInput(attrs={"class": "input", "placeholder": "auditourim"}),
            "phone_no": forms.TextInput(attrs={"class": "input", "placeholder": "9714548761"}),
            "password": forms.TextInput(attrs={"class": "grow", "placeholder": "Create password"}),
            "club_name": forms.TextInput(attrs={"class": "input", "placeholder": "Enter Club Name"}),
            "no_of_slots": forms.NumberInput(attrs={"class": "input", "placeholder": "No. of slot available"}),

            "volunteer_name": forms.TextInput(attrs={"class": "input", "placeholder": "organizers name"}),
            "volunteer_phone_no": forms.TextInput(attrs={"class": "input", "placeholder": "organizers Phone no"}),
            "volunteer_position": forms.TextInput(attrs={"class": "input", "placeholder": "organizers position in club"}),

            "img": forms.ClearableFileInput(
                attrs={"accept": "image/*", "class": "input", "placeholder": "upload your event pic:",
                       "type": "file"}),
            "img_2": forms.ClearableFileInput(
                attrs={"accept": "image/*", "class": "input", "placeholder": "upload your event pic:",
                       "type": "file"}),
            "img_3": forms.ClearableFileInput(
                attrs={"accept": "image/*", "class": "input", "placeholder": "upload your event pic:",
                       "type": "file"}),
            "img_4": forms.ClearableFileInput(
                attrs={"accept": "image/*", "class": "input", "placeholder": "upload your event pic:",
                       "type": "file"}),

            "registion_opening_date": forms.DateInput(attrs={"class":"input","placeholder":"YYYY-MM-DD","id":"jsPickr"}),
            "registion_closing_date": forms.DateInput(
                attrs={"class": "input", "placeholder": "YYYY-MM-DD", "id": "jsPickr"}),
            "event_starting_time": forms.TimeInput(
                attrs={"class": "input", "placeholder": "HH-MM", "id": "time-picker","type":"time"}),
            "registion_on_date":forms.DateInput(
                attrs={"class": "input", "placeholder": "YYYY-MM-DD", "id": "jsPickr"}),

            "event_type": forms.RadioSelect(attrs={"class":"radio radio-primary",}),

            "event_details":forms.Textarea(attrs={"class":"textarea min-h-20 resize-none","id":"userBio","placeholder":"enter details about your event"}),
            "amount": forms.TextInput(attrs={"class": "input", "placeholder": "Enter price per ticket"}),

        }
