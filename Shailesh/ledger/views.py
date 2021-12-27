from django.db.models import Sum
from django.shortcuts import redirect, render, reverse
from django.views.generic import (CreateView, UpdateView, DeleteView)

from . import forms, models


def index(request):
    pending_list = models.Client.objects.all()
    total = 0
    date_per = models.DateSelector.objects.get(pk=1)
    for client in pending_list:
        closing_bal = models.Trancation.objects.filter(client_id=client,
                                                       booking_date__lt=date_per.end_date).aggregate(
            sum=Sum('amount')
        )
        # print(closing_bal['sum'])
        closing_bal['sum'] = closing_bal['sum'] if closing_bal['sum'] else 0
        client.val = closing_bal['sum']
        total = total + closing_bal['sum']
    return render(request, "ledger/dashboard.html", {
        'pending': pending_list,
        'total': total,
        'date': date_per
    })

class FirmCreateView(CreateView):
    model = models.Firm
    form_class = forms.FirmForm

    def get_success_url(self):
        return reverse('index')

class ClientCreateView(CreateView):
    model = models.Client
    form_class = forms.ClientForm

    def get_success_url(self):
        return reverse('add-trancation', kwargs={'id': self.object.id})


class ClientUpdateView(UpdateView):
    model = models.Client
    form_class = forms.ClientForm

    def get_success_url(self):
        return reverse('add-trancation', kwargs={'id': self.object.id})


class TranctionCreateListView(CreateView):
    model = models.Trancation
    form_class = forms.TrancationForm

    def get_context_data(self, **kwargs):
        context = super(TranctionCreateListView, self).get_context_data(
            **kwargs)
        client_id = self.kwargs.get('id')
        client = models.Client.objects.get(pk=client_id)
        date_period = models.DateSelector.objects.get(pk=1)
        opening_bal = models.Trancation.objects.filter(client_id=client_id,
                                                       booking_date__lt=date_period.start_date).aggregate(
            sum=Sum('amount'))
        closing_bal = models.Trancation.objects.filter(client_id=client_id,
                                                       booking_date__lt=date_period.end_date).aggregate(
            sum=Sum('amount')
        )
        pbal = models.Trancation.objects.filter(client_id=client_id,
                                                booking_date__gte=date_period.start_date,
                                                booking_date__lte=date_period.end_date,
                                                amount__gt=0).aggregate(sum=Sum('amount'))
        # print(pbal)
        nbal = models.Trancation.objects.filter(client_id=client_id,
                                                booking_date__gte=date_period.start_date,
                                                booking_date__lte=date_period.end_date,
                                                amount__lt=0).aggregate(sum=Sum('amount'))
        # print(nbal)
        pbal['sum'] = pbal['sum'] if pbal['sum'] else 0
        opening_bal['sum'] =  opening_bal['sum'] if opening_bal['sum'] else 0
        total =  pbal['sum'] + opening_bal['sum']
        nbal['sum'] = nbal['sum'] if nbal['sum'] else 0
        total_d = total + nbal['sum']
        context['client'] = client
        context['open_bal'] = opening_bal
        context['close_bal'] = closing_bal
        context['date'] = date_period
        context['trancations'] = models.Client.objects.get(pk=client_id)
        context['pbal'] = total
        context['nbal'] = total_d
        return context

    def form_valid(self, form):
        pk = self.kwargs['id']
        form.instance.client = models.Client.objects.get(pk=pk)
        # print(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add-trancation', kwargs={'id': self.kwargs['id']})


class TranctionUpadateListView(UpdateView):
    model = models.Trancation
    form_class = forms.TrancationForm

    def get_context_data(self, **kwargs):
        context = super(TranctionUpadateListView, self).get_context_data(
            **kwargs)
        context['trancations'] = models.Client.objects.get(
            pk=self.kwargs.get('client_id'))
        return context

    def form_valid(self, form):
        pk = self.kwargs['client_id']
        form.instance.client = models.Client.objects.get(pk=pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add-trancation',
                       kwargs={'id': self.kwargs['client_id']})


def client_list_view(request):
    client_list = models.Client.objects.all()
    for client in client_list:
        val = 0
        for tranction in client.trancation_set.all():
            val += tranction.amount
        client.val = val
    return render(request, 'ledger/client_list.html',
                  {'client_list': client_list})


def client_detail_view(request, id):
    client_details = models.Trancation.objects.filter(client_id=id)
    return render(request, 'ledger/client_detail.html', {
        'client_details': client_details
    })


def update_entry_verified(request, client_id, id):
    trancation = models.Trancation.objects.get(pk=id)
    trancation.verifed = not trancation.verifed
    trancation.save()
    return redirect('add-trancation', id=client_id)


def client_report(request, id, client_id, firm):
    fi = models.Firm.objects.get(pk=firm)
    tran = models.Trancation.objects.get(pk=id, firm_id=firm)
    opening_bal = models.Trancation.objects.filter(client_id=client_id, firm_id=firm,
                                                   booking_date__lt=tran.booking_date).aggregate(
        sum=Sum('amount'))
    trancation = models.Trancation.objects.filter(client_id=client_id, firm_id=firm,
                                                  booking_date__gte=tran.booking_date)
    total_due = 0
    total_rec = 0
    _is_credit = False
    if opening_bal['sum'] != None:
        if opening_bal['sum'] > 0:
            total_due += opening_bal['sum']
        else:
            total_rec += opening_bal['sum']
    for t in trancation:
        if t.amount > 0:
            total_due += t.amount
        else:
            _is_credit = True
            total_rec += t.amount
    client = models.Client.objects.get(pk=client_id)
    return render(request, 'ledger/client_print.html', {
        'open': opening_bal['sum'],
        'tran': trancation,
        'client': client,
        'total_due': total_due,
        'total_rec': total_due + total_rec,
        'is_credit': _is_credit,
        'firm':fi,

    })


def ledger_of_client(request, id):
    f = 0
    trancation=trancation = models.Trancation.objects.filter(client_id=id)
    firm = models.Firm.objects.all()
    if request.method == 'POST':
        f = request.POST['firm_selected']
        print(request.POST['firm_selected'])
        trancation = models.Trancation.objects.filter(client_id=id, firm_id=f)    
    client = models.Client.objects.get(pk=id)
    balance = 0
    for t in trancation:
        balance += t.amount
        t.bal = balance


    return render(request, 'ledger/ledger_report.html', {
        'tran': trancation,
        'client': client,
        'firm': firm,
        'f': f
    })


def from_to_report(request, id):
    client = models.Client.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.FromToForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['from_date'] > form.cleaned_data['to_date']:
                return render(request, 'ledger/from_to.html', {'form': form,
                                                               'client': client})
            opening_bal = models.Trancation.objects.filter(client_id=id,
                                                           booking_date__lt=
                                                           form.cleaned_data[
                                                               'from_date']).aggregate(
                sum=Sum('amount'))
            trancation = models.Trancation.objects.filter(client_id=id,
                                                          booking_date__gte=
                                                          form.cleaned_data[
                                                              'from_date'],
                                                          booking_date__lte=
                                                          form.cleaned_data[
                                                              'to_date'])
            total_due = 0
            total_rec = 0
            total = 0
            _is_credit = False
            if opening_bal['sum'] != None:
                if opening_bal['sum'] > 0:
                    total_due += opening_bal['sum']
                else:
                    total_rec += opening_bal['sum']
            for t in trancation:
                if t.amount > 0:
                    total_due += t.amount
                else:
                    _is_credit = True
                    total_rec += t.amount

            return render(request, 'ledger/client_print.html', {
                'open': opening_bal['sum'],
                'tran': trancation,
                'client': client,
                'total_due': total_due,
                'total_rec': total_due + total_rec,
                'is_credit': _is_credit
            })
        else:
            print("form not valid")
    else:
        form = forms.FromToForm()
        return render(request, 'ledger/from_to.html', {'form': form,
                                                       'client': client})


class TranctionDeleteView(DeleteView):
    model = models.Trancation

    def get_success_url(self):
        return reverse('add-trancation',
                       kwargs={'id': self.kwargs['client_id']})


class DateSelectUpdateView(UpdateView):
    model = models.DateSelector
    form_class = forms.DateSelectorForm

    def get_success_url(self):
        return reverse('index')


class DateSelectCreateView(CreateView):
    model = models.DateSelector
    form_class = forms.DateSelectorForm

    def get_success_url(self):
        return reverse('index')
