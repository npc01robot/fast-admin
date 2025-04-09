from collections import defaultdict

from celery import shared_task
from django.db import transaction

from finance.models import ExternalLoan, Loan


@shared_task
def update_external_loans(data):
    # Extract loan_ids from the incoming data
    ids = [item["loan_id"] for item in data]

    # Create dictionaries to keep track of the loans to update or create
    existing_loans = defaultdict(list)
    create_list = []
    update_list = []

    external_loans = ExternalLoan.objects.filter(
        loan_id__in=ids,
        start_date__in=[item["start_date"] for item in data],
        end_date__in=[item["end_date"] for item in data]
    ).values("loan_id", "start_date", "end_date", "id", "actual_cost")

    for loan in external_loans:
        existing_loans[(loan["loan_id"], loan["start_date"].strftime("%Y-%m-%d"), loan["end_date"].strftime("%Y-%m-%d"))] = loan

    for item in data:
        loan_key = (item["loan_id"], item["start_date"], item["end_date"])

        if loan_key in existing_loans:
            external_loan = existing_loans[loan_key]
            if external_loan["actual_cost"] != item["actual_cost"]:
                existing_loans[loan_key]["actual_cost"] = item["actual_cost"]
                update_list.append(ExternalLoan(id=external_loan["id"], actual_cost=item["actual_cost"]))
        else:
            create_list.append(ExternalLoan(
                loan_id=item["loan_id"],
                start_date=item["start_date"],
                end_date=item["end_date"],
                actual_cost=item["actual_cost"]
            ))

    with transaction.atomic():
        if update_list:
            ExternalLoan.objects.bulk_update(update_list, ["actual_cost"])
        if create_list:
            ExternalLoan.objects.bulk_create(create_list)

