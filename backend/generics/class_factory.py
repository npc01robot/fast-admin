from external_guarantee.models import ExternalGuarantee
from external_guarantee.models import ExternalBeGuaranteed


def create_class(class_name):
    return globals()[class_name]()
