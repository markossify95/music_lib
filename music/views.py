from django.contrib.auth.models import User
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Album
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  # LOGIN DAJE SESSION ID !!!!!!!!
from django.views.generic import View
from .forms import UserForm

'''
FUNKCIJE KOJE UZIMAJU ZAHTEVE KORISNIKA I VRACAJU NESTO
UGLAVNOM PRIMAJU HTTP GET/POST REQUEST etc. i VRACAJU HTTP RESPONSE
'''

# Create your views here.

"""
# funkcija koja vraca index stranicu

def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    return render(request, 'music/index.html', context)


''' OVO JE NACIN SA INSIDE HTML-om, ALI POENTA JE DA SE URADI SA IZOLOVANIM FRONTOM //TEMPLATES
def index(request):
    all_albums = Album.objects.all()
    html = ''
    for album in all_albums:
        url = '/music/' + str(album.id) + '/'
        html += '<a href= "' + url + '">' + album.album_title + '</a><br>'
    return HttpResponse(html)  # U ZAGRADAMA MOZE BILO KOJI TEXT ILI HTML KOD!!!
'''


# funkcija vraca detalje o albumu

def detail(request, album_id):
    ''' TEZI NACIN:
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not exist in database!")
    return render(request, 'music/detail.html', {'album': album})  # NAJKVALITETNIJA LINIJA!
    '''
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album': album,
            'error_message': "SONG SELECTION NOT VALID"})
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})

"""


# GENERICKI VIEW-OVI RADE SA KLASAMA (umesto sa funkcijama) I PREDSTAVLJAJU NA LEPSI NACIN UZ MANJE KODA

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'  # GOVORI NAM KAKO SE OBRACAMO REZULTATIMA IZ TEMPLATE

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']  # polja iz baze u okviru liste


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # prikazuje prazan form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # ubacuje u bazu
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()

            # returns User object if everything is OK
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})
