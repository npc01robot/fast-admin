from rest_framework import serializers

from auth_ext.models.department import Department
from finance.cache_loan import refresh_loan_cache
from finance.models import Finance, Loan, LoanRepay, LoanInterest


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    "授信名称"
    credit_name = serializers.ReadOnlyField(source="credit.name")
    "授信code"
    credit_code = serializers.ReadOnlyField(source="credit.code")
    "授信金融机构"
    credit_organization = serializers.ReadOnlyField(source="credit.organization")
    "授信金额"
    credit_amount = serializers.ReadOnlyField(source="credit.amount")
    last_repay_date = serializers.SerializerMethodField(read_only=True)
    last_interest_date = serializers.SerializerMethodField(read_only=True)

    def get_last_repay_date(self, obj):
        repay = LoanRepay.objects.filter(loan=obj, is_deleted=False).last()
        if repay:
            return repay.repay_date
        else:
            return ""

    def get_last_interest_date(self, obj):
        interest = LoanInterest.objects.filter(loan=obj, is_deleted=False).last()
        if interest:
            return interest.interest_date
        else:
            return ""

    class Meta:
        model = Loan
        fields = [
            "id",
            "credit",
            "credit_name",
            "credit_code",
            "credit_organization",
            "credit_amount",
            "loan_unit",
            "name",
            "type",
            "loan_amount",
            "loan_balance",
            "contract_rate",
            "overall_rate",
            "deposit_rate",
            "actual_rate",
            "is_fixed_rate",
            "margin_rate",
            "origin_interest_amount",
            "guarantee_way",
            "guarantee_unit",
            "anti_guarantee_way",
            "anti_guarantee_unit",
            "loan_date",
            "actual_interest",
            "due_date",
            "sign_date",
            "debt_file",
            "repay_amount",
            "last_repay_date",
            "last_interest_date",
            "interest",
            "is_deposit",
            "agent_user",
            "remark",
            "repay_interest",
            "create_user",
            "update_user",
            "create_time",
            "update_time",
        ]

    def validate(self, attrs):
        if attrs.get("loan_amount") <= 0:
            raise serializers.ValidationError("贷款金额必须大于0")
        credit = attrs.get("credit")
        credit_amount = credit.amount
        if attrs.get("loan_amount") > credit_amount:
            raise serializers.ValidationError("贷款金额必须小于等于授信金额")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        dept = user.dept
        if dept:
            dept = Department().get_top_departments(user.dept)
            validated_data["dept"] = dept.id
        loan = Loan.objects.create(**validated_data)
        credit = loan.credit
        credit.surplus_amount -= loan.loan_amount
        credit.save()
        refresh_loan_cache.delay()
        return loan


class LoanRepaySerializer(serializers.ModelSerializer):
    loan_unit = serializers.ReadOnlyField(source="loan.loan_unit", help_text="贷款单位")
    loan_name = serializers.ReadOnlyField(source="loan.name", help_text="贷款名称")
    loan_type = serializers.ReadOnlyField(source="loan.type", help_text="贷款类型")
    debt_file = serializers.ReadOnlyField(source="loan.debt_file", help_text="债务文件")
    sign_date = serializers.ReadOnlyField(source="loan.sign_date", help_text="签订日期")
    loan_amount = serializers.ReadOnlyField(
        source="loan.loan_amount", help_text="贷款金额"
    )
    loan_repay_amount = serializers.ReadOnlyField(
        source="loan.repay_amount", help_text="已还金额"
    )
    due_amount = serializers.SerializerMethodField(read_only=True, help_text="到期金额")
    due_date = serializers.ReadOnlyField(source="loan.due_date", help_text="到期日期")
    interest_repay_amount = serializers.SerializerMethodField(
        read_only=True, help_text="利息"
    )

    def get_due_amount(self, obj):
        return obj.loan.loan_amount - obj.loan.repay_amount

    def get_interest_repay_amount(self, obj):
        return obj.loan.loan_balance * obj.loan.overall_rate

    class Meta:
        model = LoanRepay
        fields = [
            "id",
            "loan",
            "loan_id",
            "loan_unit",
            "loan_name",
            "loan_type",
            "debt_file",
            "sign_date",
            "loan_amount",
            "loan_repay_amount",
            "due_amount",
            "due_date",
            "interest_repay_amount",
            "repay_date",
            "repay_amount",
            "voucher_number",
            "repay_source",
            "remark",
            "create_user",
            "update_user",
            "create_time",
            "update_time",
        ]

    def validate(self, attrs):
        if attrs.get("repay_amount") <= 0:
            raise serializers.ValidationError("还款金额必须大于0")
        loan = attrs.get("loan")
        if attrs.get("repay_amount") >= loan.balance - loan.repay_amount:
            raise serializers.ValidationError("还款金额必须小于等于待还金额")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        dept = user.dept
        if dept:
            dept = Department().get_top_departments(user.dept)
            validated_data["dept"] = dept.id
        loan = validated_data.get("loan")
        repay_amount = validated_data.get("repay_amount")
        loan.repay_amount += repay_amount
        loan.save()
        repay = LoanRepay.objects.create(**validated_data)
        return repay


class LoanInterestSerializer(serializers.ModelSerializer):
    loan_unit = serializers.ReadOnlyField(source="loan.loan_unit", help_text="贷款单位")
    loan_name = serializers.ReadOnlyField(source="loan.name", help_text="贷款名称")
    loan_type = serializers.ReadOnlyField(source="loan.type", help_text="贷款类型")
    debt_file = serializers.ReadOnlyField(source="loan.debt_file", help_text="债务文件")
    sign_date = serializers.ReadOnlyField(source="loan.sign_date", help_text="签订日期")
    loan_amount = serializers.ReadOnlyField(
        source="loan.loan_amount", help_text="贷款金额"
    )
    loan_repay_amount = serializers.ReadOnlyField(
        source="loan.repay_amount", help_text="待还利息"
    )
    loan_repay_interest = serializers.ReadOnlyField(
        source="loan.repay_interest", help_text="已还利息"
    )
    due_amount = serializers.SerializerMethodField(read_only=True, help_text="到期金额")
    due_date = serializers.ReadOnlyField(source="loan.due_date", help_text="到期日期")
    interest_repay_amount = serializers.SerializerMethodField(
        read_only=True, help_text="利息"
    )

    def get_due_amount(self, obj):
        return obj.loan.loan_amount - obj.loan.repay_amount

    def get_interest_repay_amount(self, obj):
        return obj.loan.loan_balance * obj.loan.overall_rate

    class Meta:
        model = LoanInterest
        fields = [
            "id",
            "loan",
            "loan_id",
            "loan_unit",
            "loan_name",
            "loan_type",
            "debt_file",
            "sign_date",
            "loan_amount",
            "loan_repay_amount",
            "loan_repay_interest",
            "due_amount",
            "due_date",
            "interest_repay_amount",
            "interest_date",
            "interest_amount",
            "voucher_number",
            "interest_source",
            "remark",
            "create_user",
            "update_user",
            "create_time",
            "update_time",
        ]

    def validate(self, attrs):
        if attrs.get("interest_amount") <= 0:
            raise serializers.ValidationError("利息金额必须大于0")
        loan = attrs.get("loan")
        if attrs.get("interest_amount") > loan.actual_interest:
            raise serializers.ValidationError("利息金额必须小于等于待还利息")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        dept = user.dept
        if dept:
            dept = Department().get_top_departments(user.dept)
            validated_data["dept"] = dept.id
        loan = validated_data.get("loan")
        interest_amount = validated_data.get("interest_amount")
        loan.repay_interest += interest_amount
        loan.save()
        interest = LoanInterest.objects.create(**validated_data)
        return interest
