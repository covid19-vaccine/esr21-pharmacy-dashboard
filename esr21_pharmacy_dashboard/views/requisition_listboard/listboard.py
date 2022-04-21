from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, \
    SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from esr21_pharmacy.models import DrugAccountabilityLog
from ...model_wrappers import RequisitionsModelWrapper, \
    AccountabilityModelWrapper


class RequisitionsViews(NavbarViewMixin, EdcBaseViewMixin,
                        ListboardFilterViewMixin, SearchFormViewMixin,
                        ListboardView):
    listboard_template = 'esr21_pharma_requisitions_listboard_template'
    listboard_url = 'pharma_requisitions_listboard'
    listboard_fa_icon = 'fas fa-vial'
    listboard_panel_style = 'info'
    model = 'esr21_pharmacy.drugrequisition'
    model_wrapper_cls = RequisitionsModelWrapper
    navbar_name = 'esr21_pharmacy_dashboard'
    navbar_selected_item = 'esr21_pharmacy'
    search_form_url = 'pharma_requisitions_listboard'

    @property
    def drug_accountability_cls(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_obj = DrugAccountabilityLog()

        accountability_model_wrapper = AccountabilityModelWrapper(
            model_obj=model_obj
        )
        drug_req_obj = self.model_cls()
        wrapped_drug_req_obj = self.model_wrapper_cls(
            model_obj=drug_req_obj
        )

        context.update(
            add_accountability_href=accountability_model_wrapper.href,
            requisition=wrapped_drug_req_obj
        )
        return context
