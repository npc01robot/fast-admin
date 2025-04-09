from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta, datetime

from auth_ext.models.department import Department
from finance.cache_loan import get_loan_cache
from finance.tasks import update_external_loans
from generics.models import ImportExportRecord
from generics.tasks import export_handle_task
from finance.filters import (
    LoanFilter,
    LoanRepayFilter,
    LoanInterestFilter,
)
from finance.models import Loan, LoanRepay, LoanInterest, ExternalLoan
from finance.serializers import (
    LoanSerializer,
    LoanRepaySerializer,
    LoanInterestSerializer,
)

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.filter(is_deleted=False).all()
    serializer_class = LoanSerializer
    filterset_class = LoanFilter
    def get_queryset(self):
        user = self.request.user
        if user.dept:
            dept_top = Department().get_top_departments(user.dept)
            return self.queryset.filter(dept=dept_top.id)
        else:
            return self.queryset.all()


    @action(detail=False, methods=["get"])
    def export(self, request, *args, **kwargs):
        user = request.user
        query_params = request.query_params.dict()

        export_handle_task.delay(
            ImportExportRecord.LOAN,
            user.id,
            **query_params,
            class_name="Loan",
        )
        return Response({"message": "Export task has been submitted."})

    @action(detail=False, methods=["get"])
    def home_data(self, request, *args, **kwargs):
        dict_data = get_loan_cache()
        return Response(dict_data)

    @action(detail=False, methods=["get"])
    def export_home_data(self, request, *args, **kwargs):
        dict_data = get_loan_cache()

        return Response(dict_data)
    # 一年内到期融资金额
    @action(detail=False, methods=["get"])
    def one_year_repay_amount(self, request, *args, **kwargs):
        today = datetime.today()
        one_year_age = today + timedelta(days=365)
        queryset = (
            Loan.objects.filter(
                due_date__gte=today,
                due_date__lte=one_year_age,
                is_deleted=False,
            )
            .all()
            .order_by("-due_date")
        )
        serializer = LoanSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    @action(detail=False, methods=["post"])
    def save_external_loan(self, request, *args, **kwargs):
        data = request.data
        update_external_loans(data)
        return Response({"message": "保存成功！"})

    @action(detail=False, methods=["post"])
    def external_loan(self, request, *args, **kwargs):
        data = request.data
        loan_ids = [item["loan_id"] for item in data]
        start_dates = [item["start_date"] for item in data]
        end_dates = [item["end_date"] for item in data]

        # 批量查询 ExternalLoan 数据
        external_loans = ExternalLoan.objects.filter(
            loan_id__in=loan_ids,
            start_date__in=start_dates,
            end_date__in=end_dates
        )

        # 使用字典缓存查询结果，以提高查询效率
        loan_map = {
            (loan.loan_id, loan.start_date.strftime("%Y-%m-%d"), loan.end_date.strftime("%Y-%m-%d")): loan
            for loan in external_loans
        }

        result = []
        for item in data:
            # 通过元组（loan_id, start_date, end_date）查找对应的外部贷款信息
            loan_key = (item["loan_id"], item["start_date"], item["end_date"])
            external_loan = loan_map.get(loan_key)

            if external_loan:
                result.append({
                    "loan_id": item["loan_id"],
                    "actual_cost": external_loan.actual_cost,
                })
        return Response(result)

class LoanRepayViewSet(viewsets.ModelViewSet):
    queryset = LoanRepay.objects.filter(is_deleted=False).all()
    serializer_class = LoanRepaySerializer
    filterset_class = LoanRepayFilter

    def get_queryset(self):
        user = self.request.user
        if user.dept:
            dept_top = Department().get_top_departments(user.dept)
            return self.queryset.filter(dept=dept_top.id)
        else:
            return self.queryset.all()


    @action(detail=False, methods=["get"])
    def export(self, request, *args, **kwargs):
        user = request.user
        query_params = request.query_params.dict()

        export_handle_task.delay(
            ImportExportRecord.REPAYMENT,
            user.id,
            **query_params,
            class_name="LoanRepay",
        )
        return Response({"message": "Export task has been submitted."})


class LoanInterestViewSet(viewsets.ModelViewSet):
    queryset = LoanInterest.objects.filter(is_deleted=False).all()
    serializer_class = LoanInterestSerializer
    filterset_class = LoanInterestFilter

    def get_queryset(self):
        user = self.request.user
        if user.dept:
            dept_top = Department().get_top_departments(user.dept)
            return self.queryset.filter(dept=dept_top.id)
        else:
            return self.queryset.all()

    @action(detail=False, methods=["get"])
    def export(self, request, *args, **kwargs):
        user = request.user
        query_params = request.query_params.dict()

        export_handle_task.delay(
            ImportExportRecord.INTEREST,
            user.id,
            **query_params,
            class_name="LoanInterest",
        )
        return Response({"message": "Export task has been submitted."})
