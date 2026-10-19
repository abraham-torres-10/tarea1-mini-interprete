import pytest
from mini_interprete.cli import interpretar
from mini_interprete.errores import ErrorDeEvaluacion, ErrorDeSintaxis


def test_suma():
    assert interpretar("3 + 4") == 7


def test_resta():
    assert interpretar("10 - 3") == 7


def test_multiplicacion():
    assert interpretar("6 * 7") == 42


def test_division():
    assert interpretar("10 / 2") == 5


def test_precedencia_sin_parentesis():
    assert interpretar("3 + 4 * 2") == 11


def test_precedencia_con_parentesis():
    assert interpretar("(3 + 4) * 2") == 14


#Casos normales
def test_operaciones_combinadas_con_parentesis():
    assert interpretar("((2 + 3) * 4) + 1") == 21

def test_suma_y_resta_combinadas():
    assert interpretar("10 + 5 - 3") == 12


#Casos frontera

# Se debe asociar a la izquierda: (10 - 3) - 2 = 5
def test_resta_encadenada_asociatividad_izquierda():
    assert interpretar("10 - 3 - 2") == 5

# El resultado debe ser: 10 / 4 = 2.5
def test_division_decimal_exacta():
    assert interpretar("10 / 4") == 2.5

# Según la semántica '007' es 7
def test_numero_con_ceros_a_la_izquierda():
    assert interpretar("007 + 3") == 10

# Se debe reportar como ErrorDeEvaluacion
def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("10 / 0")


#Entradas inválidas

# Con la semántica declarada, -3 es inválido y lanza ErrorDeSintaxis
def test_menos_unario_no_soportado():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-3")

# Una expresión con paréntesis sin cerrar lanza ErrorDeSintaxis
def test_parentesis_sin_cerrar():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("(3 + 4")
