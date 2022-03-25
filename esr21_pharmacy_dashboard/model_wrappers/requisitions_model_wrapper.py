from django.conf import settings
from edc_model_wrapper import ModelWrapper
from .accountability_model_wrapper_mixin import AccountabilityModelWrapperMixin


class RequisitionsModelWrapper(AccountabilityModelWrapperMixin, ModelWrapper):
    model = 'esr21_pharmacy.drugrequisition'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pharma_requisitions_listboard')
    querystring_attrs = ['tracking_identifier']
    next_url_attrs = ['tracking_identifier']
