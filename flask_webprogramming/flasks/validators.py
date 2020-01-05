import datetime
from wtforms import Form, BooleanField, TextField, PasswordField, validators,\
                    StringField, Field, ValidationError


class RegistrationForm(Form):
    userid = TextField('SV.userid', [validators.Length(min=5, max=13)], \
        id='useris')
    username = TextField('SV.username', [validators.Length(min=4)])
    password1 = PasswordField('SV.password1', [validators.DataRequired(),\
        validators.EqualTo('password2',\
            message='Server: Password1과 Password2가 다릅니다.')])
    password2 = PasswordField('SV.password2', [validators.DataRequired()])
    # mail = TextField('SV.mail', [validators.Email(message='not is valid'), \
    #       validators.Length(min=6, max=35)])
    # phoneNumber = TextField('SV.phoneNumber', [validators.Regexp('([0-9])', \
    #       message='Server: only numbers.')])
    # post1 = TextField('우편번호1', [validators.InputRequired(), \
    #       KoreaPostValidator()])
    # tel1 = TextField('지역번호', [validators.InputRequired(), \
    #       KoreaRegionTelValidator()])
    # hp1 = TextField('휴대폰 첫 번째 번호', [validators.InputRequired(), \
    #       KoreaMobileTelValidator()])
    # ksn1 = TextField('주민등록번호 앞자리', [validators.InputRequired(), \
    #       KoreaSocialNumberValidator('ksn2')])
    # ksn2 = TextField('주민등록번호 뒷자리', [validators.InputRequired()])
    # credit_number = TextField('신용카드번호', [validators.InputRequired(), \
    #       CreditCardNumValidator()])
    # credit_year = TextField('연도', [validators.InputRequired(), \
    #       CreditCardExpiresValidator('credit_month')])
    # credit_month = TextField('월', [validators.InputRequired()])

def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)
    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise validators.ValidatationError(message)
    return _length

class MyForm(Form):
    name = StringField('Name', [validators.InputRequired(), length(max=50)])
    def validate_name(form, field):
        if len(field.data) > 50:
            raise validators.ValidatationError(
                'Name must be less than 50 characters.'
            )

class Length(object):
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'Field must be between %i and %i characters long' \
                    % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = len(field.data) if field.data else 0
        if l < self.min or self.max != -1 and l > self.max:
            raise validators.ValidatationError(self.message)
       
class KoreaPostValidator():
    def __init__(self, message=None):
        if not message:
            message = u'올바른 우편번호가 아닙니다.'
        self.message = message
    
    def __call__(self, form, field):
        post2_field_data = form[self.post2_field].data

        # raise error if postno starts with 0
        if field.data.startswith("0"):
            validators.ValidationError(self.message)
        
        # raise error if postno less than 5
        if len(field.data) < 5:
            validators.ValidationError(self.message)

class KoreaRegionTelValidator():
    def __init__(self, message=None):
        if not message:
            message = u'올바른 지역번호가 아닙니다.'
        self.message = message

        self.area_title_number = (
            "02", "031", "032", "033",
            "041", "042", "043", "044", "049",
            "051", "052", "053", "054", "055",
            "061", "062", "063", "064", "070"
        )

    def __call__(self, form, field):
        if field.data not in self.area_title_number:
            validators.ValidationError(self.message)
        
class KoreaMobileTelValidator():
    def __init__(self, message=None):
        if not message:
            message = u'올바른 휴대폰 번호가 아닙니다.'
        self.message = message
        self.mobie_title_number = (
            "010", "011", "016", "017", "018", "019"
        )

        def __call__(self, form, field):
            if field.data not in self.mobie_title_number:
                validators.ValidationError(self.message)

class KoreaSocialNumberValidator():
    def __init__(self, ksn2_field, message=None):
        if not message:
            message = u'올바른 주민등록번호가 아닙니다.'
        self.message = message
        self.ksn2_field = ksn2_field

    def __call__(self, form, field):
        ksn1_value = field.data
        ksn2_value = form[self.ksn2_field].data

        ksn2_value, check_digit = ksn2_value[:-1], ksn2_value[-1]

        ksn_number = "{0}{1}".format(ksn1_value, ksn2_value)
        check_magic_number = "234567892345"

        ksn_magic_number = sum(
            [int(real) * int(check) for real, check\
                in zip(ksn_number, check_magic_number)]
        )

        check_prg1 = (11 - (ksn_magic_number % 11)) % 10
        if check_prg1 != int(check_digit):
            validators.ValidationError(self.message)

class CreditCardNumValidator():
    def __init__(self, message=None):
        if not message:
            message = u'올바른 신용카드번호가 아닙니다.'
        self.message = message
    
    def __call__(self, form, field):
        hol = jjak = 0

        credit_card_num = field.data.replace(" ", "")

        for i, value in enumerate(credit_card_num, 1):
            if i % 2 == 1:
                tmp = int(value) * 2
                if tmp >= 10:
                    str_tmp = str(tmp)
                    tmp = int(str_tmp[0]) + int(str_tmp[1])
                hol += tmp
            else:
                jjak += int(value)
            
        if ((hol + jjak) % 10) != 0:
            validators.ValidationError(self.message)

class CreditCardExpiresValidator():
    def __init__(self, expire_month_field, message=None):
        if not message:
            message = u'올바른 신용카드 유효일자가 아닙니다.'
        self.message = message
        self.expire_month_field = expire_month_field
    
    def __call__(self, form, field):
        expire_month = int(form[self.expire_month_field].data)
        expire_year = int(field.data)

        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)

        next_month = expire_month % 12 + 1
        next_month_year = expire_year

        if next_month == 1:
            next_month_year += 1
        
        exprire_date = datetime.date(next_month_year, next_month, 1)

        # raise error if input date is before present time
        if exprire_date < today:
            validators.ValidationError(self.message)