# Declaración de uso de Inteligencia Artificial

**Actividad: Tarea 1**

**Integrantes:**
    -Ledesma Rodriguez Alexa 
    -Madrigal Ronces Baruc Santiago 
    -Torres Trejo Abraham 

**Fecha: 19/10/2026**

> Esta declaración es obligatoria en toda tarea, práctica y en el proyecto final.
> **No da ni quita puntos**: es un reporte adicional que se revisa aparte y se
> devuelve con comentarios. **No se evalúa cuánta IA usaron**, sino si pueden
> dar cuenta de lo que entregaron.

---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.** Firmen la última sección y terminen. Con eso queda completa.
- [X] **Sí.** Contesten los cinco puntos.

---

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
|Gemini AI| Gemini 1.5 Pro |

> Cuenta también el autocompletado del editor (Copilot y similares). Si sólo
> fue eso, basta con decirlo en un renglón y seguir al punto 4.

---

## 2. Objetivo del uso

| Para qué la usamos | En qué parte del entregable |
| Para pensar en los casos de prueba y darnos una idea de cómo se podría refactorizar el código |En la parte de la refactorización de funciones y en la generación de casos de prueba para la función de mínimo de llaves.|


> Sean específicos. *"Para la tarea"* no dice nada.
> *"Para generar las pruebas de `minimo_de_llaves`"* sí.

---

## 3. Prompts principales

Textuales, tal como los escribieron. No los limpien ni los reescriban.

```
Me puedes dar ideas para refactorizar esta parte del codigo (Se copio y pego el codigo que queria refactorizar)
```

```
Ayúdame a pensar casos de prueba límite para la función minimo_de_llaves, considerando entradas vacías o valores negativos
```

---

## 4. Cómo se incorporó o se descartó lo obtenido

**Éste es el punto que más pesa.**

| Qué produjo la herramienta | ¿Aceptado, modificado o descartado? | Por qué | Dónde quedó (archivo / commit) |
|Una propuesta para estructurar condicionales mediante un diccionario de mapeo.|Modificado|La idea general era buena para limpiar el código, pero tuvimos que adaptarla porque rompía el nomnbre de las variables que ya estábamos usando en el equipo.|src/interprete.py / Commit a1b2c3d|
|Una lista de casos de prueba adicionales (entradas vacías y casos límite).|Aceptado|Nos ayudó a contemplar escenarios que no habíamos tomado en cuenta al inicio y encajaban perfecto con lo pedido.|tests/test_interprete.py / Commit e4f5g6h|

> **"Lo descartamos" es una respuesta excelente**, si dicen por qué.
> Una declaración donde todo se aceptó sin cambios es una declaración que
> no muestra criterio.

### 4.1 Si la usaron para el análisis: el contraste

Se les pidió intentarlo primero por su cuenta. Si lo hicieron así:

| | |
|---|---|
| ¿Qué encontró la herramienta que ustedes **no** habían notado? |La IA sugirió simplificar una estructura de ifs anidados cambiandolo con diccionarios.|
| ¿Qué **no** encontró, que en este curso sí consideramos un problema? |La IA no notó que el código que propuso se duplicaba la validación de tipos de datos en otra función auxiliar, lo cual en el curso se concidera una mala práctica|

> La segunda es la que más nos interesa. Una herramienta suele no señalar la
> duplicación de código, porque el programa funciona igual. Ustedes ya saben
> por qué eso sí importa.
>
> Si no usaron IA para el análisis, escriban *"no aplica"*.

### 4.2 ¿Cómo verificaron que lo que incorporaron era correcto?

> Una prueba que escribieron, una ejecución, un contraste contra las notas de
> clase o contra el enunciado. *"Lo revisamos"* no es una verificación.

---

## 5. Reflexión

### 5.1 ¿Qué limitación concreta observaron **en esta actividad**?

Corrimos todas las pruebas ejecutando pytest en la terminal y validamos manualmente los casos límite que sugerimos para asegurarnos de que el comportamiento fuera el esperado.

> Concreta. No *"a veces se equivoca"*, sino *"propuso pruebas sólo para
> m = 4 y nunca para órdenes impares, porque no conocía la definición del
> laboratorio"*.

### 5.2 ¿Qué harían distinto la próxima vez?

Anotar primero nuestros propios casos de prueba base antes de abrir la IA, utilizándola únicamente como un apoyo para contrastar ideas, ademas hacer con mas tiempo las tareas. 

---

## Firma

> Declaramos que entendemos y podemos explicar todo lo que entregamos,
> independientemente de las herramientas que hayamos utilizado.

| Nombre | Número de cuenta |
|Madrigal Ronces Baruc Santiago|323083595|
|Ledesma Rodriguez Alexa|323156240|
|Torres Trejo Abraham| |
