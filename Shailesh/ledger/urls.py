from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('add-client/', views.ClientCreateView.as_view(), name='add-client'),
    path('add-tranction/<int:id>', views.TranctionCreateListView.as_view(),
         name='add-trancation'),
    path('client-list/', views.client_list_view, name='client-list'),
    path('client-detail/<int:id>', views.client_detail_view,
         name='client-detials'),
    path('client-detail-update/<int:pk>/<int:client_id>',
         views.TranctionUpadateListView.as_view(), name='tran-update'),
    path('client-detail-verifed/<int:id>/<int:client_id>/',
         views.update_entry_verified,
         name='verifed-entry'),
    path('client-report/<int:id>/<int:client_id>', views.client_report,
         name='client-report'),
    path('client-ledger/<int:id>', views.ledger_of_client,
         name='client-ledger'),
    path('from-to/<int:id>', views.from_to_report,
         name='from-to'),
    path('delete/<int:pk>/<int:client_id>',
         views.TranctionDeleteView.as_view(), name='delete-tranction'),
    path('update-client/<int:pk>', views.ClientUpdateView.as_view(),
         name='update-client')
]
