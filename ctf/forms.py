import time
from django import forms
from django.core.exceptions import ValidationError
from .models import Flag, Participant, Submission
from ctf.models import CUSTOM_NAME_REGEX, FLAG_SECRET_REGEX


class SubmissionForm(forms.Form):
    participant = forms.ModelChoiceField(Participant.objects.all(
    ), empty_label="Select...", help_text="Your username or groupname")
    name = forms.CharField(max_length=40, required=False, validators=[
                           CUSTOM_NAME_REGEX], help_text="Additional info visible on the leaderboard")
    secret = forms.CharField(max_length=200, validators=[FLAG_SECRET_REGEX])

    def clean_secret(self):
        data = self.cleaned_data["secret"]
        flag_model = Flag.objects.filter(secret=data).first()
        if not flag_model:
            time.sleep(3)  # Brute-force protection
            raise ValidationError("Unknown secret!")
#        else:
#            participant = self.cleaned_data["participant"]
#            participant_model = Participant.objects.filter(name=participant).first()
#            print(f" { participant } with { participant_model.points } points just scored an extra { flag_model.points } points")
#            participant_model.points = participant_model.points + flag_model.points
#            print(f" { participant } now has { participant_model.points } points")
#            participant_model.save()
#            print("Trying something else...")
#            participant.save()
        return data

    def clean(self):
        cleaned_data = super().clean()
        flag = Flag.objects.filter(secret=cleaned_data.get("secret")).first()
        participant = cleaned_data.get("participant")
        if Submission.objects.filter(flag=flag, participant=participant).exists():
            raise ValidationError("Flag already submitted!")
        return cleaned_data
