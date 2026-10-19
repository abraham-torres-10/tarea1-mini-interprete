# Análisis — Tarea 1

**Integrantes:**
1.
2.
3.

**Fork:**
**Rama:**

> Contesten en este archivo. Respuestas breves y concretas: se califica que
> hayan entendido, no la extensión.

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` | | | |
| `parser` | | | |
| `ast` | | | |
| `evaluator` | | | |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

> Usen `(3 + 4) * 2` como ejemplo y muestren cómo se ve entre etapa y etapa.

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens | |
| AST | |
| resultado | |

> Para el renglón del AST, dibújenlo **primero ustedes** y después comprueben
> con `python3 interprete.py --arbol "(3 + 4) * 2"`. Si su dibujo y el del
> programa no coinciden, uno de los dos está mal, y averiguar cuál es
> justamente el trabajo.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| | | | | |

> Llenen la tabla **completa**, con las 13. Es tediosa a propósito: la única
> forma de saber qué no está cubierto es caracterizar sistemáticamente lo que
> sí. Cuando terminen, léanla como columna, no como renglones, y pregúntense
> qué combinación **no aparece nunca**.

### 2.2 ¿Qué comportamientos **no** estaban probados?

> Ésta es la pregunta importante de toda la tarea. Tómense su tiempo.

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| tests/test_evaluator.py::test_operaciones_combinadas_con_parentesis | "((2 + 3) * 4) + 1" | 21 | Normal | Expresión válida con múltiples niveles de anidación que ejercita el flujo regular del evaluador. |
| tests/test_evaluator.py::test_suma_y_resta_combinadas | "10 + 5 - 3" | 12 | Normal | Flujo regular de sumas y restas con operadores en el mismo nivel sin anidaciones complejas. |
| tests/test_evaluator.py::test_resta_encadenada_asociatividad_izquierda | "10 - 3 - 2" | 5 | Frontera | Encadenamiento de operadores de la misma precedencia; prueba si se asocian a la izquierda como exige la semántica declarada. |
| tests/test_evaluator.py::test_division_decimal_exacta | "10 / 4" | 2.5 | Frontera | Verifica que la división produzca un valor real no entero según la semántica (float). |
| tests/test_evaluator.py::test_numero_con_ceros_a_la_izquierda | "007 + 3" | 10 | Frontera | Caso límite en la representación de enteros: 007 debe interpretarse como 7. |
| tests/test_evaluator.py::test_division_entre_cero | "10 / 0" | ErrorDeEvaluacion | Frontera | Caso límite matemático; debe lanzar el error semántico propio del intérprete. |
| tests/test_evaluator.py::test_menos_unario_no_soportado | "-3" | ErrorDeSintaxis | Inválida | La especificación declara que no existe el menos unario, debiendo rechazarse con ErrorDeSintaxis. |
| tests/test_evaluator.py::test_parentesis_sin_cerrar | "(3 + 4" | ErrorDeSintaxis | Inválida | Entrada mal formada sintácticamente; debe reportarse como ErrorDeSintaxis y no con una excepción de Python. |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

El defecto principal revelado fue la **asociatividad incorrecta (a la derecha en vez de a la izquierda)** en operadores de la misma precedencia. Al evaluar una resta encadenada como `"10 - 3 - 2"`, el parser la agrupaba recursivamente hacia la derecha como `10 - (3 - 2)` dando `9`. 
Adicionalmente, se reveló un segundo defecto: ante expresiones con paréntesis abiertos sin cerrar (como `"(3 + 4"`), el parser intentaba leer más allá de la lista de tokens arrojando un error interno de Python (`IndexError: list index out of range`).

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

Comparado directamente contra la tabla de **Semántica declarada** (Sección 7 del `README.md`):
1. **Regla de Asociatividad:** *"los operadores de la misma precedencia se asocian a la izquierda"*. El código original hacía llamadas recursivas en `derecha = self._expresion()` y `derecha = self._termino()`, construyendo árboles sesgados a la derecha.
2. **Regla de Entrada inválida:** *"debe rechazarse con ErrorDeSintaxis, nunca con un error de Python"*. Dejar escapar un `IndexError` incumple el contrato de manejo de errores del intérprete.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| Asociatividad a la derecha en sumas/restas y productos | `"10 - 3 - 2"` | `9` | `5` | `commit de pruebas` | `commit de corrección` |
| `IndexError` no capturado ante paréntesis sin cerrar | `"(3 + 4"` | `IndexError` | `ErrorDeSintaxis` | `commit de pruebas` | `commit de corrección` |

En `src/mini_interprete/parser.py`:
- Se modificaron `_expresion()` y `_termino()` para sustituir la recursión derecha por un ciclo `while` acumulador (`expresion := termino (('+' | '-') termino)*`). Cada iteración toma el subárbol anterior como hijo izquierdo (`nodo = OperacionBinaria(operador, nodo, derecha)`), garantizando asociatividad a la izquierda.
- En `_factor()` se validó si `_actual()` es `None` o diferente de `PAR_DER` antes de avanzar, lanzando explícitamente `ErrorDeSintaxis` en lugar de provocar un desbordamiento de índice.

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

Porque la solución implementa de forma exacta la gramática declarada en el encabezado de `parser.py`:`expresion := termino (('+' | '-') termino)*`.
El ciclo while permite encadenar cualquier cantidad de operaciones seguidas (como a - b - c - d ...), agrupándolas de izquierda a derecha de forma general, sin trucos ni reglas especiales para casos particulares. Todas las 13 pruebas iniciales y las 8 nuevas pasan con éxito.
---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

1. **Duplicación de código algorítmico en `Parser` (`_expresion` vs `_termino`):**
   Ambos métodos repetían exactamente la misma lógica de control para operadores binarios asociativos a la izquierda: evaluar el término base, verificar en un bucle si el siguiente token coincide con una tupla de operadores, avanzar consumiendo el operador, evaluar el subárbol derecho en el nivel inferior y reasignar el subárbol acumulado a la izquierda. Lo único que cambiaba era la tupla de operadores (`OPERADORES_SUMA` vs `OPERADORES_PRODUCTO`) y la función del nivel inferior llamada (`_termino` vs `_factor`). Esto violaba el principio DRY (*Don't Repeat Yourself*).

2. **Rigidez y condicionales repetidos en `evaluator.py` (Violación de Open-Closed Principle):**
   En `evaluar()`, la ejecución de cada operación matemática dependía de una serie de condicionales `if nodo.operador == "+": ... if nodo.operador == "-": ...`. Esta estructura es rígida: para extender el sistema con una nueva operación aritmética es necesario modificar directamente el método existente añadiendo más bifurcaciones en lugar de extenderlo mediante una estructura como una tabla de despacho (diccionario de funciones).

3. **Amplificación del cambio (*Shotgun Surgery*):**
   Agregar un simple operador aritmético nuevo requiere tocar prácticamente todos los módulos del proyecto: `tokens.py` (definición del enum), `lexer.py` (asociación de símbolo textual), `parser.py` (reglas gramaticales y precedencia) y `evaluator.py` (evaluación numérica).

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

Se aplicó la técnica **Extract Method** en [parser.py](file:///home/abraham/tercero/modelado/tarea1-mini-interprete/src/mini_interprete/parser.py), creando un método auxiliar generalizado:
```python
def _binaria(self, regla_siguiente, operadores):
    izquierda = regla_siguiente()
    while self._actual() is not None and self._actual().tipo in operadores:
        operador = self._avanzar()
        derecha = regla_siguiente()
        izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
    return izquierda
```
Con esto, `_expresion()` y `_termino()` se redujeron a delegar limpiamente en una sola línea pasando su función siguiente y su conjunto de operadores:
- `_expresion`: `return self._binaria(self._termino, OPERADORES_SUMA)`
- `_termino`: `return self._binaria(self._factor, OPERADORES_PRODUCTO)`

**Por qué conserva el comportamiento:**
El cambio es matemáticamente y algorítmicamente equivalente. `_binaria` ejecuta exactamente la misma secuencia de instrucciones que ejecutaba el código duplicado en el mismo orden: lee el nodo de la izquierda llamando a `regla_siguiente()`, evalúa la condición del `while` con `_actual()`, consume el token con `_avanzar()`, lee la derecha llamando a `regla_siguiente()` y construye la misma instancia de `OperacionBinaria` asignándola a la izquierda. Los 21 casos de prueba pasan sin ninguna alteración.

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

**Respuesta: Ninguno es pertinente.**

- **Adapter:** No aplica. El patrón Adapter se utiliza para permitir que dos clases con interfaces incompatibles colaboren entre sí (comúnmente al integrar bibliotecas de terceros o sistemas legacy). En este intérprete todos los componentes (`lexer`, `parser`, `ast`, `evaluator`) fueron creados para trabajar en conjunto desde el inicio; sus interfaces ya encajan de forma natural y directa (listas de tokens y nodos de AST).
- **Factory Method:** No aplica. Factory Method es útil cuando la lógica de instanciación debe delegarse a subclases polimórficas que varían según el contexto. En este proyecto la instanciación de nodos (`Numero`, `OperacionBinaria`) y de tokens (`Token`) es directa y concisa mediante sus constructores estándar. Añadir jerarquías de fábricas abstractas y creadores concretos generaría **complejidad accidental** e indirecciones innecesarias sin aportar ningún beneficio real de extensibilidad.

Como señala el propio README: *"un patrón que no mejora nada, resta"*. El criterio de diseño en este caso favorece la simplicidad.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

Habría que modificar **4 archivos**:
1. `tokens.py`: declarar el nuevo valor en `TipoToken` (ej. `MODULO = "MODULO"`).
2. `lexer.py`: asociar el carácter en el diccionario `SIMBOLOS` (ej. `"%": TipoToken.MODULO`).
3. `parser.py`: definir su lugar en la gramática y su precedencia.
4. `evaluator.py`: implementar la operación matemática (ej. `izquierda % derecha`) y validar posibles errores (como módulo entre cero).

**La parte más compleja y sensible es el Parser (`parser.py`)**, porque si el nuevo operador tiene una precedencia distinta a las existentes (por ejemplo, el operador de potencia `^` que tiene mayor precedencia que el producto y además asocia a la derecha), no basta con agregarlo a una tupla existente: es necesario introducir un nuevo nivel jerárquico en la gramática, agregar un nuevo método y ajustar el encadenamiento de llamadas entre niveles.

---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué *no* encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. *"No usamos"* es una declaración válida y completa; *"lo
descartamos porque..."* es de las mejores respuestas posibles.
