from django.conf import settings

from edc_model_wrapper import ModelWrapper


class AccountabilityModelWrapper(ModelWrapper):
    model = 'esr21_pharmacy.drugaccountabilitylog'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pharma_requisitions_listboard')
    next_url_attrs = ['tracking_identifier']
    querystring_attrs = ['tracking_identifier', 'injection_site',
                         'quantity_order']
