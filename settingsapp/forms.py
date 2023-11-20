from django import forms
from signuplogin.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'is_active', 'is_verified', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        # Add Tailwind CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'py-2 px-3 pe-11 block w-full border-gray-200 shadow-sm rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600'
        
        # Customize labels and placeholders if needed
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        
        # Customize widget for is_active, is_verified, is_superuser fields if needed
        self.fields['is_active'].widget.attrs['class'] = 'inline-block mt-2.5'
        self.fields['is_verified'].widget.attrs['class'] = 'inline-block mt-2.5'
        self.fields['is_superuser'].widget.attrs['class'] = 'inline-block mt-2.5'

        # You can also add labels for each field here if required
        self.fields['is_active'].label = 'Is Active'
        self.fields['is_verified'].label = 'Is Verified'
        self.fields['is_superuser'].label = 'Is Superuser'


from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import TemplateAttachment, EmailTemplate, EmailSignature
from attachments.models import Attachment
from multiupload.fields import MultiFileField
from attachments.forms import AttachmentForm

class EmailSignatureForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = EmailSignature
        fields = ['name', 'content']

class EmailTemplateForm(forms.ModelForm):
    attachments = MultiFileField(min_num=0, max_num=5, max_file_size=1024 * 1024 * 5, required=False)

    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body']

    body = forms.CharField(widget=CKEditorWidget())

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()

        attachments = self.cleaned_data.get('attachments')
        if attachments:
            for attachment in attachments:
                attachment_instance = Attachment(file=attachment)
                attachment_instance.save()
                instance.templateattachment_set.create(attachment=attachment_instance)

        return instance