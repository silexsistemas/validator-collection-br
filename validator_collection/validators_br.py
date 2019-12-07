import re
import numpy as np
from errors_br import *

CELLPHONE_REGEX = re.compile(
    r'\(?([0]?[1-9][0-9])\)?\s?(9)?\s?((9|8|7)\d{3})\s?-?\s?(\d{4})$'
)
ALPHANUMERIC_REGEX = re.compile(
    r'^[a-zA-Z0-9_]+$'
)

CPF_REGEX = re.compile(
    r"/\d{3}\.?\d{3}\.?\d{3}\-?\d{2}/"
)

CNPJ_REGEX = re.compile(
    r"[0-9]{2}\.?[0-9]{3}\.[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}"
)

CNJ_REGEX = re.compile(
    r"[0-9]{7}\-[0-9]{2}\.[0-9]{4}\.[0-9]{1}\.[0-9]{2}\.[0-9]{4}"
)

def validator_cpf(value,
                  allow_empty=False,
                  ):

    # check empty
    if not value and not allow_empty:
        return "O campo está vazio"
        raise errors.EmptyValueError()
    elif not value:
        return "O campo está vazio, mas ele não é obrigatório"

    # check datatype and regex
    if not isinstance(value, str):
        return "O valor digitado não é uma string"
        raise errors_br.DataTypeError()
    else:
        is_valid = CPF_REGEX.search(value)

        if not is_valid:
            return "Inválido pelo REGEX"
            raise errors_br.InvalidCpfError()

    cpf = value

    # defining the two vectors of validation --> http://www.macoratti.net/alg_cpf.htm
    lista_validacao_um = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    cpf = cpf.replace("-", "")
    cpf = cpf.replace(".", "")

    # extract the verifying digits as string for later comparison
    verificadores = cpf[-2:]

    # transforms the str into a list of characters
    cpf = list(cpf)
    # verifying the lenght of the cpf

    # Verificar mínimo
    if len(cpf) < 11:
        return "O valor tem menos de 11 dígitos"
        raise errors.MinimumValueError()

    # Verificar máximo
    if len(cpf) > 11:
        return "O valor tem mais de 11 dígitos"
        raise errors.MaximumValueError()

    # casts each character to int
    cpf = [int(i) for i in cpf]

    # calculating the first digit
    cabeca = cpf[:9]
    dot_prod_1 = np.dot(cabeca, lista_validacao_um)
    dig_1_seed = dot_prod_1 % 11

    if dig_1_seed < 2:
        digito_1 = 0
    else:
        digito_1 = 11 - dig_1_seed

    # calculating the second digit
    cabeca.append(digito_1)
    dot_prod_2 = np.dot(cabeca, lista_validacao_dois)
    dig_2_seed = dot_prod_2 % 11

    if dig_2_seed < 2:
        digito_2 = 0
    else:
        digito_2 = 11 - dig_2_seed

    digito_1 = str(digito_1)
    digito_2 = str(digito_2)

    # returnig
    if not bool(verificadores == digito_1 + digito_2):
        return "CPF inválido"
        raise errors_br.InvalidCpfError()

    return True

def validator_cnpj(value,
                  allow_empty=False,
                  ):
    """
    Method to validate brazilian cpfs
    Parameters:
        - value (str) - The value to validate.
        - allow_empty (boll) - If True, returns None if value is empty. If False, returns EmptyValueError.

    Returns:
        - True or false

    Raises:
        - EmptyValueError – if value is None and allow_empty is False
        - MinimumValueError – if minimum is supplied and value is less than the 11 characters
        - MaximumValueError – if maximum is supplied and value is more than the 11 characters
        - DataTypeError – If value not is String
        - InvalidCnpjError – If value not is valid cpf
    """
    # check empty
    if not value and not allow_empty:
        raise errors.EmptyValueError()
    elif not value:
        return None

    # check datatype and regex
    if not isinstance(value, str):
        raise errors_br.DataTypeError()
    else:
        is_valid = CNPJ_REGEX.search(value)

        if not is_valid:
            raise errors_br.InvalidCnpjError()

    cnpj = value

    # defining the two vectors of validation --> http://www.macoratti.net/alg_cpf.htm
    lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    cnpj = cnpj.replace("-", "")
    cnpj = cnpj.replace(".", "")
    cnpj = cnpj.replace("/", "")

    # extract the verifying digits as string for later comparison
    verificadores = cnpj[-2:]

    # transforms the str into a list of characters
    cnpj = list(cnpj)
    # verifying the lenght of the cnpj

    # Verificar mínimo
    if len(cnpj) < 14:
        raise errors.MinimumValueError()

    # Verificar máximo
    if len(cnpj) > 14:
        raise errors.MaximumValueError()

    # casts each character to int
    cnpj = [int(i) for i in cnpj]

    # calculating the first digit
    cabeca = cnpj[:9]
    dot_prod_1 = np.dot(cabeca, lista_validacao_um)
    dig_1_seed = dot_prod_1 % 11

    if dig_1_seed < 2:
        digito_1 = 0
    else:
        digito_1 = 11 - dig_1_seed

    # calculating the second digit
    cabeca.append(digito_1)
    dot_prod_2 = np.dot(cabeca, lista_validacao_dois)
    dig_2_seed = dot_prod_2 % 11

    if dig_2_seed < 2:
        digito_2 = 0
    else:
        digito_2 = 11 - dig_2_seed

    digito_1 = str(digito_1)
    digito_2 = str(digito_2)

    # returnig
    return bool(verificadores == digito_1 + digito_2)

def validator_email(value,
                    allow_empty=True,
                    ):
    """
    Method to validate e-mail

    Email address validation is...complicated. The methodology that we have
    adopted here is *generally* compliant with
    `RFC 5322 <https://tools.ietf.org/html/rfc5322>`_ and uses a combination of
    string parsing and regular expressions.
    String parsing in particular is used to validate certain *highly unusual*
    but still valid email patterns, including the use of escaped text and
    comments within an email address' local address (the user name part).
    This approach ensures more complete coverage for unusual edge cases, while
    still letting us use regular expressions that perform quickly.

    Parameters:
        - value (str) - The value to validate.
        - allow_empty (boll) - If True, returns None if value is empty. If False, returns EmptyValueError.

    Returns:
        - True or false

    Raises:
        - EmptyValueError – if value is None and allow_empty is False
        - DataTypeError – If value not is String
        - InvalidEmailError – If value not is valid e-mail
    """
    if validators.email(value) == value:
        return True

def validator_cnj(value,
                  allow_empty=False,
                  ):
    """
    Method to validate brazilian cpfs
    Parameters:
        - value (str) - The value to validate.
        - allow_empty (boll) - If True, returns None if value is empty. If False, returns EmptyValueError.

    Returns:
        - True or false

    Raises:
        - EmptyValueError – if value is None and allow_empty is False
        - MinimumValueError – if minimum is supplied and value is less than the 20 characters
        - MaximumValueError – if maximum is supplied and value is more than the 20 characters
        - DataTypeError – If value not is String
        - InvalidCnjError – If value not is valid cpf
    """
    # check empty
    if not value and not allow_empty:
        raise errors.EmptyValueError()
    elif not value:
        return None

    # whitespace_padding
    value = value.strip()

    cnj_caracteres = value
    cnj_caracteres = cnj_caracteres.replace("-", "")
    cnj_caracteres = cnj_caracteres.replace(".", "")

    # transforms the str into a list of characters
    cnj_caracteres = list(cnj_caracteres)
    # Verificar mínimo
    if len(cnj_caracteres) < 20:
        raise errors.MinimumValueError()

    # Verificar máximo
    if len(cnj_caracteres) > 20:
        raise errors.MaximumValueError()

    # check datatype and regex
    if not isinstance(value, str):
        raise errors_br.DataTypeError()
    else:
        is_valid = CNJ_REGEX.search(value)

        if not is_valid:
            raise errors_br.InvalidCnjError()

    # Estabelecendo variáveis
    cnj_number = value
    NNNNNNN = cnj_number.split('-')[0]
    DD = cnj_number.split('.')[0].split('-')[1]
    AAAA = cnj_number.split('.')[1]
    J = cnj_number.split('.')[2]
    J_dict = {'1': 'STF', '2': 'CNJ', '3': 'STJ', '4': 'Justiça Federal', '5': 'Justiça do Trabalho',
              '6': 'Justiça Eleitoral', '7': 'Jutiça Militar da União', '8': 'Justiça Estadual',
              '9': 'Justiça Militar Estadual'}
    J_extenso = J_dict[J]
    TR = cnj_number.split('.')[3]
    OOOO = cnj_number.split('.')[4]

    # Inicialmente, os dígitos verificadores D1 D0 devem ser deslocados para o final do número do processo e
    # receber valor zero
    s = NNNNNNN + AAAA + J + TR + OOOO
    s_00 = s + '00'

    # Os dígitos de verificação D1 D0 serão calculados pela aplicação da seguinte fórmula, na qual “módulo” é a
    # operação “resto da divisão inteira”:
    # D1D0 = 98 – (N6N5N4N3N2N1N0A3A2A1A0J2T1R0O3O2O1O00100 módulo 97)
    digits = str(98 - (int(s_00) % 97))

    # se o resultado tiver apenas 1 digito, colocar 0 à esquerda
    if len(digits) == 1:
        digits = '0' + digits

    # Para a validação dos dígitos basta aplicar a seguinte fórmula: = (N6N5N4N3N2N1N0A3A2A1A0J2T1R0O3O2O1O00100 módulo 97). Se o resultado da fórmula for 1, os dígitos de verificação estão corretos. Isto significa que existe uma probabilidade aproximada de 99,4% de que não tenham sido cometidos erros de digitação, situação que atinge o objetivo principal do projeto.
    s_DD = s + DD
    digits_DD = str((int(s_DD) % 97))

    if digits_DD == '1':
        return True
    else:
        raise errors_br.InvalidCnjError()

def in_list(value, values_list):
    if len(values_list) == 0:
        raise errors.EmptyValueError('The list cannot be empty')
    if value not in values_list:
        raise NotInListError('The {value} is not in the list'.format(value=value))

def cellphoneValidator(value, allow_empty=False):
    '''
    Validate that 'value' is a Brazilian Cellphonenumber

    :param value: The value to validate.

    :param allow_empty:
    If ``True``, returns :obj:`None <python:None>` if ``value`` is empty.
    If ``False``, raises a :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
    if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    if value is None and allow_empty:
        return None
    elif value is None or value == "":
        raise errors.EmptyValueError('value cannot be None')
    '''
    if CELLPHONE_REGEX.search(value):
        return True
    else:
        return False

def alphanumericValidator(value, allow_empty=False):
    '''
    Validate that 'value' contains alphanumeric digits.

    :param value: The value to validate.

    :param allow_empty:
    If ``True``, returns :obj:`None <python:None>` if ``value`` is empty.
    If ``False``, raises a :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
    if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    if value is None and allow_empty:
        return None
    elif value is None or value == "":
        raise errors.EmptyValueError('value cannot be None')
    '''
    if ALPHANUMERIC_REGEX.match(value):
        return True
    else:
        return False