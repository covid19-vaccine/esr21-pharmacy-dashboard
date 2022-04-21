from django.urls import path

from .views import RequisitionsViews, AccountabilityLog, DashboardView, DrugDisposal, \
    ChainOfCustody, TempExcursionReport, DailyTempLog

app_name = 'esr21_pharmacy_dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home_url'),
    path('requisitions/', RequisitionsViews.as_view(),
         name='pharma_requisitions_listboard'),
    path('accountability/', AccountabilityLog.as_view(),
         name='accountability_log_listboard_url'),
    path('download/drug_disposal_form/', DrugDisposal),
    path('download/chain_of_custody_form/', ChainOfCustody),
    path('download/temp_excursion_report/', TempExcursionReport),
    path('download/dail_temp_log/', DailyTempLog),
    path('dropdown_menu_form/', AccountabilityLog.as_view(),
         name='dropdown_menu_form')
    ]
