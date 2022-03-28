from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, \
    SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from esr21_pharmacy.models import DrugAccountabilityLog
from ...model_wrappers import AccountabilityModelWrapper


class AccountabilityLog(NavbarViewMixin, EdcBaseViewMixin,
                        ListboardFilterViewMixin, SearchFormViewMixin,
                        ListboardView):
    listboard_template = 'esr21_pharma_accountability_log_listboard_template'
    listboard_url = 'pharma_accountability_log_listboard'
    listboard_panel_style = 'info'
    # listboard_fa_icon = "fa-user-plus"
    #     listboard_view_filters = ListboardViewFilters()
    model = 'esr21_pharmacy.drugaccountabilitylog'
    model_wrapper_cls = AccountabilityModelWrapper
    navbar_name = 'esr21_pharmacy_dashboard'
    navbar_selected_item = 'esr21_pharmacy'
    search_form_url = 'pharma_accountability_log_listboard'

    @property
    def accountability_cls(self):
        return django_apps.get_model(self.model_wrapper_cls.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_obj = DrugAccountabilityLog()

        accountability_model_wrapper = AccountabilityModelWrapper(
            model_obj=model_obj
            )
        context.update(
            add_accountability_href=accountability_model_wrapper.href,
            )
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('status'):
            statuses = (request.POST.get('status'))
            status, lot_number = statuses.split(',')

            try:
                change_obj = self.accountability_cls.objects.get(
                    lot_number=lot_number,
                    )
            except self.accountability_cls.DoesNotExist:
                pass

            else:
                change_obj.status = status
                change_obj.save()

        return self.get(request, *args, **kwargs)
