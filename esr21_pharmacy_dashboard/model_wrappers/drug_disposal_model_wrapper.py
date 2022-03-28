from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DrugDisposalModelWrapper(ModelWrapper):
    model = 'esr21_pharmacy.drugdisposal'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'esr21_pharma_dashboard_url')
