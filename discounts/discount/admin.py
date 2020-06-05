from django.contrib import admin
from django import forms
from django.http import Http404
from .models import *
import gettext
import time


class PeriodInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()
        if not any([form.has_changed() for form in self.forms]):
            raise forms.ValidationError(
                gettext.gettext('Agreement should have at least one period'),
                code='empty_periods'
            )
        agr = None
        for form in self.forms:
            if form.has_changed():
                agr = form.instance.related_agreement
        agr_start = agr.start_date
        agr_stop = agr.stop_date
        timestamps = []
        for form in self.forms:
            t1 = form.cleaned_data.get('start_date')
            t2 = form.cleaned_data.get('stop_date')
            if not form.has_changed():
                continue
            if t1 == None and t2 == None:
                continue
            if t1 == None:
                raise forms.ValidationError(
                    gettext.gettext('Please, set period start date'),
                    code='empty_start_date'
                )
            if t2 == None:
                raise forms.ValidationError(
                    gettext.gettext('Please, set period stop date'),
                    code='empty_stop_date'
                )
            if t1 > t2:
                raise forms.ValidationError(
                    gettext.gettext('Period can not stop before it starts'),
                    code='non_causal_period'
                )
            if t1 == t2:
                raise forms.ValidationError(
                    gettext.gettext('Period should have non-zero duration'),
                    code='zero_period'
                )
            if t1 < agr_start:
                raise forms.ValidationError(
                    gettext.gettext('Period can not start before its \
                    agreement does'),
                    code='early_period'
                )
            if t2 > agr_stop:
                raise forms.ValidationError(
                    gettext.gettext('Period can not stop after its \
                    agreement does'),
                    code='late_period'
                )
            to_unix_tstamp = lambda t: int(time.mktime(t.timetuple()))
            """
            Implementation of the period intersections checking:
            1) putting all dates of start and stop into one list
            2) sorting this list in such way, that if start and stop date are equal,
            stop date comes before the start date (periods with
            zero duration are not allowed)
            3) scanning the list and searching whether one period begins before another ends
            """
            timestamps += [
                (to_unix_tstamp(t1), 1), (to_unix_tstamp(t2), 0)
            ]
        timestamps.sort(
            key=lambda stamp: stamp[0] + stamp[1]
        )
        k = 0
        for stamp in timestamps:
            if k > 1:
                raise forms.ValidationError(
                    gettext.gettext('Periods should not intersect'),
                    code='period_intersection'
                )
            if stamp[1]:
                k += 1
            else:
                k -= 1


class PeriodInline(admin.TabularInline):
    model = Period
    extra = 1
    formset = PeriodInlineFormSet
    ordering = ('-stop_date',)


class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = '__all__'

    def clean_debit(self):
        if self.cleaned_data["debit"] < 0:
            raise forms.ValidationError(
                gettext.gettext('Debit should be grater than or equal to zero'),
                code='wrong_debit'
            )
        return self.cleaned_data["debit"]

    def clean_credit(self):
        if self.cleaned_data["credit"] < 0:
            raise forms.ValidationError(
                gettext.gettext('Credit should be grater than or \
                equal to zero'),
                code='wrong_credit'
            )
        return self.cleaned_data["credit"]

    def clean(self):
        if self.cleaned_data['start_date'] > self.cleaned_data['stop_date']:
            raise forms.ValidationError(
                gettext.gettext('Agreement can not stop before it starts'),
                code='non_causal_agreement'
            )
        return self.cleaned_data


class AgreementAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['company', 'negotiator']}),
        ('Financial information', {'fields': ['debit', 'credit']}),
        ('Date information', {'fields': ['start_date', 'stop_date']})
    ]
    inlines = [PeriodInline,]
    form = AgreementForm
    list_display = (
        'company', 'negotiator', 'start_date', 'stop_date', 'debit', 'credit'
    )
    list_filter = ['company', 'company__country', 'negotiator']
    search_fields = [
        'negotiator__first_name', 'negotiator__last_name', 'company__title',
        'company__country__name', 'company__country__code'
    ]
    ordering = ('-stop_date',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country')
    list_filter = ['country',]
    search_fields = ['title', 'country__name', 'country__code']


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


admin.site.register(Country, CountryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Agreement, AgreementAdmin)
