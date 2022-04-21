from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DailyTempLogUploadModelWrapper(ModelWrapper):
    model = 'esr21_pharmacy.dailytemplogupload'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'esr21_pharma_dashboard_url')
