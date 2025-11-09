from django.shortcuts import render
from .forms import userRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth import logout
def register(request):#cree un compte 
    if request.method == 'POST':#bech nabathdonc envoie nestamel methode post
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')#baad ma ykml el inscription yrouhou lel page mta3 login
    else:
        form = userRegistrationForm()#hethi kenha get
    return render(request, 'register.html', {'form': form})#render trajaa 3 hajet request template w contexte format dictionnaire fih el variable form eli bech nasta3mlouha fel template

def logout_view(req):
    logout(req)
    return redirect('login')
