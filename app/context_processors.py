from .forms import SendMailToSuperusersForm

def add_mail_form_to_context(request):
    return {"mail_form": SendMailToSuperusersForm()}
