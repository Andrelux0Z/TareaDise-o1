# Bitácora de la práctica

Estudiante:Andrés Gabriel Padilla Robles
Carné:2025137295

> Cómo se llena cada entrada, en este orden y sin saltarse pasos:
>
> 1. **Predicción** — escríbala ANTES de correr nada. Qué cree que va a
>    pasar y por qué. Equivocarse aquí y entender después vale más que
>    acertar; no vuelva a corregirla.
> 2. **Observación** — corra el experimento de la etapa y pegue la salida.
> 3. **Explicación** — por qué pasó lo que pasó, en sus palabras, citando
>    **su** archivo y **su** línea (`servicio.py:24`).
> 4. **Sello** — corra `python herramientas/marcador.py` al cerrar la
>    etapa y pegue el sello que imprime.

## Etapa 0 — Diagnóstico

**Predicción:**
Pienso que el código está hecho para que todo esté mal a propósito

**Observación:**

El código tenía muchas cosas mal.

**Explicación:**
El archivo está diseñado para violar los 11 principios que aparecen en el documento de diagnostico.

**Sello:**
3a50e5af3dd2ffdc

## Etapa 1 — Dividir y conquistar, cohesión

**Predicción:**
No entiendo qué predecir si ya leí el código en el étapa 0 y ya hice el diagnóstico.
El archivo legado mezcla 6 responsabilidades (HTTP, BD, Reglas, Validar cédula, Configuración y Registro).
Pienso que deberían haber 6 archivos, uno por cada cosa que hace el programa.

**Observación:**
Creé las carpetas dominio, aplicación e infraestructura, junto con los modelos base congelados y las clases de errores. El marcador pasó a verde

**Explicación:**
Apliqué el principio de cohesión y el de dividir y conquistar. Por ejemplo, mi archivo clinicasegura/dominio/modelos.py:3 ahora tiene una sola responsabilidad (definir los datos abstractos congelados como Cedula), desligándolo por completo del resto de las operaciones web o de base de datos.

**Sello:**
d798cb0d969441e2

## Etapa 2 — Reducir el acoplamiento

**Predicción:**
Como ya había visto en mi diagnóstico que el diccionario global CONFIG daba problemas, creo que la solución será sacar la fórmula del dinero a una función nueva, y dejar de usar diccionarios sueltos para pasar la información de la receta.

**Observación:**
Al hacer el experimento y cambiarle los días a la variable CONFIG desde la consola, vi que el sistema cambiaba las fechas de vencimiento de la nada. Esto pasa porque todo el código está leyendo ese diccionario a escondidas

**Explicación:**
Para quitar ese acoplamiento, creé la función calcular_recargo en mi nuevo archivo clinicasegura/dominio/reglas.py:3. Esto lo arregla porque la función ahora solo pide 3 datos simples para hacer su trabajo y ya no tiene que andar leyendo cosas de afuera ni diccionarios globales.

**Sello:**
8e5c2ce60d38b4de

## Etapa 3 — Abstracción y reuso

**Predicción:**
Como ya identifiqué que el JSON del proveedor se filtra por todo el sistema, predigo que al construir una interfaz limpia, esas llaves feas del JSON desaparecerán por completo de la lógica de negocio y quedarán encerradas en la infraestructura

**Observación:**
Al buscar manualmente las palabras full_name y risk_lvl en el código, veo que el modelo del proveedor está contaminandolo todo. Al terminar la etapa, esto no debería ocurrir.

**Explicación:**
Al usar la clase Protocol y nombrar los métodos por su propósito de negocio (enviar en lugar de post), se logra que el dominio hable de Despachos y no de diccionarios de red.

**Sello:**

## Etapa 4 — Flexibilidad, obsolescencia y portabilidad

**Predicción:**
Dado que el código viejo usa puros condicionales if/elif para decidir a qué farmacia enviar la receta, predigo que cuando la prueba intente usar la cadena "FarmaViva" el sistema va a fallar.

**Observación:**
Al correr la prueba, vi que efectivamente el sistema colapsó porque el orquestador principal no estaba preparado para recibir un nombre de farmacia nuevo.

**Explicación:**
Apliqué el principio de Diseñar para la flexibilidad al crear el archivo clinicasegura/infraestructura/registro.py para construir un diccionario de pasarelas, y actualicé servicio.py:12 para que busque en ese diccionario en vez de usar if/elif. Entonces si después llega una farmacia nueva, solo hay que agregar un archivo en infraestructura sin tocar la clase principal.

**Sello:**
721e8c4faf88cdcd

## Etapa 5 — Testabilidad

**Predicción:**
Predigo que va a fallar inmediatamente porque intentará crear una base de datos real en mi disco duro usando rutas que no existen, demostrando que es imposible probarlo de forma aislada.
**Observación:**
Al intentar ejecutar el código legado en la consola falló de inmediato y nisiquiera corrió. Lanzó un error porque intentó crear una base de datos real en la carpeta de Linux /tmp/. Contando los problemas, para probar una simple regla matemática me obliga a cambiar cosas del mundo real, necesito un disco duro con permisos específicos, una conexión a internet real, un reloj físico que avance y un generador de azar.

**Explicación:**
ara solucionar esto, modifiqué clinicasegura/dominio/servicio.py:6 para que el programa ya no intente conectarse a la base de datos ni pedir la hora por su cuenta. En lugar de eso, ahora recibe todo eso (el reloj, la bitácora, etc.) como parámetros en el __init__. Al pasárselos desde afuera cuando se hacen pruebas se puede poner un reloj falso y no se necesita internet.

**Sello:**
8bdfc30efaaa7481

## Etapa 6 — Diseño defensivo

**Predicción:**
Al ver que el segundo comando le agrega una bandera -O, pienso que el programa intentará correr más rápido y quizá se salte validaciones de seguridad o ignore errores para no detenerse

**Observación:**
Al correr los comandos en mi consola, el programa reventó desde el inicio por el viejo problema de la ruta en /tmp/. Sin embargo, al investigar qué hace realmente la bandera -O en Python, aprendí que borra todas las líneas que digan assert. Fui a revisar el archivo viejo y vi que usaba assert para validar las recetas, lo que significa que el programa habría dejado pasar datos maliciosos silenciosamente

**Explicación:**
Para evitar que las reglas se borren en producción, usé la librería pydantic en el nuevo archivo clinicasegura/aplicacion/borde.py. Esta herramienta obliga a validar los datos usando reglas estrictas, como decirle que el valor debe ser mayor a cero. De esta forma, si entran datos sucios, se lanza un error real y no un assert, por lo que nunca se podrá ignorar

**Sello:**
66fab1f8eb594793

## Cierre — Los principios en conflicto

Nombre dos principios que se estorbaron entre sí en SU rediseño, y con qué
criterio resolvió el conflicto. Cite el archivo donde se ve la decisión.

**Conflicto 1:**

**Conflicto 2:**
