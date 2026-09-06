# Diagnóstico del código de partida

Lea `clinicasegura/legado.py` entero antes de escribir una sola línea de
código nuevo. Llene una fila por principio. En la columna de evidencia
cite **archivo y línea** (por ejemplo `legado.py:38`); una fila sin
evidencia no cuenta.

Si cree que un principio **no** está violado, escriba la fila igual y
explique por qué en la columna de hallazgo.

| # | Principio | Hallazgo concreto | Evidencia (archivo:línea) | Qué cuesta si no se corrige |
|---|-----------|-------------------|---------------------------|------------------------------|
| 1 | Dividir y conquistar | La clase ServicioRecetas hace demasiadas cosas. Hace validaciones, cálculos, guarda en base de datos y manda peticiones web. | legado.py: 44 | Código difícil de leer y propenso a errores al agregar nuevas reglas. |
| 2 | Aumentar la cohesión | El método emitir mezcla tareas muy distintas. En lugar de hacer una sola cosa, calcula fechas, arma JSONs, y guarda registros a la vez. | legado.py: 57 | El código se vuelve un confuso y difícil de leer. Si otra parte del sistema necesita solo calcular fechas, no puede reutilizar este método. |
| 3 | Reducir el acoplamiento | Hay un diccionario global (CONFIG) que cualquier función puede leer o modificar directamente. | legado.py:30 | Si una función altera CONFIG, afectará al resto del sistema sin avisar, causando problemas difíciles de rastrear. |
| 4 | Mantener alta la abstracción | El método buscar_paciente devuelve la respuesta cruda de la API externa, obligando al resto de tu código a conocer cómo ese tercero arma su JSON | legado.py:144 | Si alguien decide cambiarle el nombre a un campo en su JSON, habría que buscar y arreglar ese cambio por todo el código. |
| 5 | Aumentar la reusabilidad | La función reporte pide el objeto "paciente" completo, cuando en realidad adentro solo usa dos datos exactos (nombre y nivel de riesgo). | legado.py:146 | Hace que la función sea inútil en otros contextos. Solo se puede usar si se le pasa ese diccionario gigante con esa misma estructura exacta. |
| 6 | Reusar lo existente | Se programó a mano la validación del formato de cédula usando bucles for y split, en lugar de usar herramientas estándar de Python. | legado.py:154 | Ese código manual requiere mantenimiento y es propenso a tener bugs tontos, las herramientas estándar ya están probadas por todos. |
| 7 | Diseñar para la flexibilidad | Para decidir a qué farmacia enviar la receta, se usa un bloque enorme de if/elif estático dentro de la función. | legado.py:79 | Cada vez que se quiera agregar una farmacia nueva, habría que abrir el código central del sistema, corriendo el riesgo de dañar las farmacias que ya sirven. |
| 8 | Anticipar la obsolescencia | El código depende directamente de librerías como sqlite3 y urllib.request metidas a la fuerza en la lógica del negocio. | legado.py:123 | Si esas librerías queden obsoletas o se decide cambiarlas por herramientas mejores, habría que reescribir mucho código en muchos lugares. |
| 9 | Diseñar para la portabilidad | El código tiene hardcodeadas las rutas C:\... y /tmp | legado.py:169 | El programa solo va a funcionar en ciertas máquinas. |
| 10 | Diseñar para la testabilidad | El código usa la hora actual dentro de la función. | legado.py:66 | Es imposible hacer pruebas automáticas consistentes. Por ejemplo, no se puede fingir que la receta ya venció para probar si el sistema responde bien. |
| 11 | Diseñar defensivamente | Se usa assert para revisar los datos de la receta y se usa except: pass para ocultar los errores si la base de datos falla. | legado.py:62 | El sistema va a dejar pasar datos malos sin tirar error y tendrá errores de base de datos sin dejar rastro de qué falló. |
