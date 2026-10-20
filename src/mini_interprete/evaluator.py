"""Del AST a un numero.

Recorre el arbol de abajo hacia arriba: para evaluar una operacion hay que
evaluar primero sus dos lados.
"""

import operator

from .ast import Numero, OperacionBinaria
from .errores import ErrorDeEvaluacion


def _dividir(izquierda, derecha):
    if derecha == 0:
        raise ErrorDeEvaluacion("division entre cero")
    return izquierda / derecha


OPERACIONES = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": _dividir,
}


def _evaluar_operacion(nodo):
    """Evalúa de forma recursiva una operación binaria."""
    operacion = OPERACIONES.get(nodo.operador)
    if operacion is None:
        raise ErrorDeEvaluacion(f"operador desconocido: {nodo.operador!r}")
    
    izquierda = evaluar(nodo.izquierda)
    derecha = evaluar(nodo.derecha)
    return operacion(izquierda, derecha)


# Mapeo de evaluadores por tipo de nodo (Idea adaptada de la IA)
EVALUADORES = {
    Numero: lambda nodo: nodo.valor,
    OperacionBinaria: _evaluar_operacion,
}


def evaluar(nodo):
    """Evalua un nodo del AST y regresa su valor."""
    evaluador = EVALUADORES.get(type(nodo))
    if evaluador is None:
        raise ErrorDeEvaluacion(f"nodo desconocido: {nodo!r}")
    
    return evaluador(nodo)