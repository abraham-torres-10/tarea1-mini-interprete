# Análisis — Tarea 1

Integrantes:
1.Ledesma Rodriguez Alexa
2.Torres Trejo Abraham
3.Madrigal Ronces Baruc Santiago 

Fork: https://github.com/abraham-torres-10/tarea1-mini-interprete.git

Rama: tarea1-pruebas-refactorizacion

> Contesten en este archivo. Respuestas breves y concretas: se califica que
> hayan entendido, no la extensión.

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` |texto | Lista de Token (tipo, valor, posición)| Reconocer números, + - * / y paréntesis, ignorar espacios y  rechazar cualquier otro carácter. No sabe nada de agrupación.|
| `parser` |Lista de Token | AST (Numero / OperacionBinaria)| Decidir cómo se agrupa la expresión de precedencia, asociatividad a la izquierda y paréntesis y rechaza la sintaxis inválida.|
| `ast` |Solo maneja datos |Nodos Numero y OperacionBinaria | Representa la estructura de la expresión sin el comportamiento, este es el contrato entre parser y evaluator.|
| `evaluator` |Un nodo del AST | Un número| Recorrer el árbol de abajo hacia arriba y calcular el valor. Reporta la división entre cero como ErrorDeEvaluacion. |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

> Usen `(3 + 4) * 2` como ejemplo y muestren cómo se ve entre etapa y etapa.

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens |[PAR_IZQ('(',0), NUMERO(3,1), MAS('+',3), NUMERO(4,5), PAR_DER(')',6), POR('*',8), NUMERO(2,10)] |
| AST | Con el hijo izquierdo + (hijos 3 y 4) e hijo derecho 2 |
| resultado | 14 |

> Para el renglón del AST, dibújenlo **primero ustedes** y después comprueben
> con `python3 interprete.py --arbol "(3 + 4) * 2"`. Si su dibujo y el del
> programa no coinciden, uno de los dos está mal, y averiguar cuál es
> justamente el trabajo.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
|test_suma|evaluator | 3 + 4 da 7| 1 | normal |
|test_resta | evaluator | 10 - 3 da 7 | 1 | normal |
|test_multiplicacion | evaluator | 6 * 7 da 42 | 1 | normal |
|test_division | evaluator | 10 / 2 da 5 | 1 | normal |
|test_precedencia_sin_parentesis | evaluator + parser | 3 + 4 * 2 da 11 | 2 distintos | normal |
|test_precedencia_con_parentesis | evaluator + parser | (3 + 4) * 2 da 14 | 2 distintos | normal |
|test_tokeniza_un_numero_solo | lexer | 42 es un token en posición 0 | 0 | frontera |
|test_tokeniza_una_suma | lexer | tipos, valores y posiciones de 3+4 | 1 | normal |
|test_los_espacios_no_producen_tokens | lexer | los espacios se ignoran | 1 | frontera |
|test_tokeniza_parentesis | lexer | ( y ) dan PAR_IZQ y PAR_DER | 0 | normal |
|test_construye_el_arbol_de_una_suma | parser | forma del AST de 3 + 4 | 1 | normal |
|test_la_multiplicacion_se_agrupa_antes_que_la_suma | parser | 3 + (4 * 2) | 2 distintos | normal |
|test_los_parentesis_cambian_la_agrupacion | parser | (3 + 4) * 2 | 2 distintos | normal | 

> Llenen la tabla **completa**, con las 13. Es tediosa a propósito: la única
> forma de saber qué no está cubierto es caracterizar sistemáticamente lo que
> sí. Cuando terminen, léanla como columna, no como renglones, y pregúntense
> qué combinación **no aparece nunca**.

### 2.2 ¿Qué comportamientos no estaban probados?

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

El defecto principal revelado fue la asociatividad incorrecta (a la derecha en vez de a la izquierda) en operadores de la misma precedencia. Al evaluar una resta encadenada como `"10 - 3 - 2"`, el parser la agrupaba recursivamente hacia la derecha como `10 - (3 - 2)` dando `9`. 
Adicionalmente, se reveló un segundo defecto: ante expresiones con paréntesis abiertos sin cerrar (como `"(3 + 4"`), el parser intentaba leer más allá de la lista de tokens arrojando un error interno de Python (`IndexError: list index out of range`).

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

Comparado directamente contra la tabla de Semántica declarada (Sección 7 del `README.md`):
1. Regla de Asociatividad: *"los operadores de la misma precedencia se asocian a la izquierda"*. El código original hacía llamadas recursivas en `derecha = self._expresion()` y `derecha = self._termino()`, construyendo árboles sesgados a la derecha.
2. Regla de Entrada inválida: *"debe rechazarse con ErrorDeSintaxis, nunca con un error de Python"*. Dejar escapar un `IndexError` incumple el contrato de manejo de errores del intérprete.

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

1. Duplicación de código algorítmico en `Parser` (`_expresion` & `_termino`):

   Ambos metodos tienen exactamente la misma estructura linea por linea: ambos primero leen el subarbol izquierdo llamando a la regla del nivel inferior, ejecutan un bucle while para ver si el token siguiente pertenece a un grupo de operadores, leen el operador + o - y pasan al siguiente elemento para continuar con la lectura, leen el subarbol izquierdo y acumulan el resultado en un nuevo nodo "Operacion binaria", esto viola el principio DRY, Si se quisiera cambiar la forma en la que s econstruyen los nodos binarios, habria que reaplicar el cambio en multiples lugares. 

2. Condicionales repetidos en evaluator.py

   En la función evaluar() había un if distinto para cada operador (+, -, *, /). Eso hace que el código sea poco flexible: cada vez que se quiera agregar una operación nueva hay que meter otro if dentro de una función que ya funciona. Es más limpio tener una tabla (un diccionario) que relacione cada símbolo con su operación, de modo que agregar un operador sea solo agregar una línea.

3. Para hacer un cambio pequeño se modifican muchos archivos 

   Agregar un operador nuevo, por ejemplo %, obliga a tocar varios archivos: tokens.py (definir el tipo de token), lexer.py (reconocer el símbolo), parser.py (decidir en qué nivel de precedencia va) y evaluator.py (calcular el resultado). Para un cambio tan pequeño son demasiados lugares, y es fácil olvidar uno. La refactorización reduce este problema solo en el evaluador, que ahora necesita una sola línea. En los demás archivos la información del operador sigue repartida.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

Qué se cambió: en evaluar() había un if por cada operador (+, -, *, /). Los sustituimos por una tabla que relaciona cada símbolo con su operación, y ahora el código busca el símbolo en la tabla en lugar de preguntar uno por uno.

Por qué el comportamiento es el mismo:

+, - y * hacen el mismo cálculo que antes, solo que mediante operator.add, operator.sub y operator.mul.
La división conserva la verificación de cero y el mismo mensaje de error (division entre cero).
Un operador desconocido sigue lanzando el mismo error.
Se siguen evaluando primero los dos lados y después se aplica el operador.

Cómo lo comprobamos: las pruebas siguen pasando, y comparamos el resultado del código original con el nuevo en varias expresiones y salió igual.

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

Ninguno es necesario.

- Adapter: sirve para conectar dos cosas que no encajan entre sí, por ejemplo cuando usamos una librería externa con otra interfaz. Aquí no hace falta, porque el lexer, el parser y el evaluador los hicimos para trabajar juntos y ya se pasan los datos directamente (tokens y nodos del AST).

- Factory Method:sirve para dejar que otra clase decida qué objeto crear. Aquí no hace falta, porque los nodos y los tokens se crean directo con su constructor (`Numero(3)`, `Token(...)`). Agregar fábricas solo complicaría el código sin darnos ninguna ventaja.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

Habría que modificar 4 archivos:
1. `tokens.py`: declarar el nuevo valor en `TipoToken` (ej. `MODULO = "MODULO"`).
2. `lexer.py`: asociar el carácter en el diccionario `SIMBOLOS` (ej. `"%": TipoToken.MODULO`).
3. `parser.py`: definir su lugar en la gramática y su precedencia.
4. `evaluator.py`: implementar la operación matemática (ej. `izquierda % derecha`) y validar posibles errores (como módulo entre cero).

La parte más compleja y sensible es el Parser (`parser.py`), porque si el nuevo operador tiene una precedencia distinta a las existentes (por ejemplo, el operador de potencia `^` que tiene mayor precedencia que el producto y además asocia a la derecha), no basta con agregarlo a una tupla existente: es necesario introducir un nuevo nivel jerárquico en la gramática, agregar un nuevo método y ajustar el encadenamiento de llamadas entre niveles.

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