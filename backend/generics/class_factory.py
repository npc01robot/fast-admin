from finance.models import Finance
from credit.models import Credit
from finance.models import Loan
from finance.models import LoanRepay
from finance.models import LoanInterest
from external_guarantee.models import ExternalGuarantee
from external_guarantee.models import ExternalBeGuaranteed


def create_class(class_name):
    return globals()[class_name]()
