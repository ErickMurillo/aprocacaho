from django.contrib import admin
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget

# Register your models here.
class InfoGeneralAdminForm(forms.ModelForm):
    texto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = InfoGeneral
        fields = ('texto',)

class InfoGeneralAdmin(admin.ModelAdmin):
    form = InfoGeneralAdminForm

class SistemaInfoAdminForm(forms.ModelForm):
    texto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = InfoGeneral
        fields = ('texto',)

class SistemaInfoAdmin(admin.ModelAdmin):
    form = SistemaInfoAdminForm

class ObjetivoAdminForm(forms.ModelForm):
    texto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Objetivo
        fields = ('texto',)

class ObjetivoAdmin(admin.ModelAdmin):
    form = ObjetivoAdminForm

class AlcanceAdminForm(forms.ModelForm):
    texto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Alcance
        fields = ('texto',)

class AlcanceAdmin(admin.ModelAdmin):
    form = AlcanceAdminForm

class ActualizacionAdminForm(forms.ModelForm):
    texto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Actualizacion
        fields = ('texto',)

class ActualizacionAdmin(admin.ModelAdmin):
    form = ActualizacionAdminForm

admin.site.register(SistemaInfo,SistemaInfoAdmin)
admin.site.register(InfoGeneral,InfoGeneralAdmin)
admin.site.register(Objetivo,ObjetivoAdmin)
admin.site.register(Alcance,AlcanceAdmin)
admin.site.register(Actualizacion,ActualizacionAdmin)
