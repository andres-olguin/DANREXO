# Issue #55 — Pruebas de salida de datos en sandbox

El sandbox de pruebas valida solicitudes con `ChatRequest`, aplica la decisión
de auditoría sintética y usa el detector `redact()` del proyecto antes de enviar
el JSON a un proveedor en memoria mediante `httpx.MockTransport`. El transporte
simulado registra las solicitudes para que pytest pueda comprobar qué recibió.

## Reproducir

Desde la raíz del repo, en un entorno virtual limpio con Python 3.14.4:

```sh
python -m pip install -r requirements-test.txt
python -m pip check
python -m pytest -q --tb=short tests/qa_egress
```

En Python 3.11 y 3.13 usa `requirements-test-compat.txt`. La instalación de
dependencias puede requerir acceso al registro de paquetes. La ejecución del
sandbox usa datos ficticios, un transporte en memoria y tokens de prueba.
El workflow `Pruebas de DELIA` recoge estos casos como parte de `tests/` y
publica sus resultados en el XML de pytest de cada versión.

## Evidencia local

La suite ampliada del sandbox obtuvo **39 casos aprobados** con las variables de
credenciales retiradas y las operaciones de red bloqueadas mediante un hook de
auditoría de Python. Los datos están en
[`tests/qa_egress/cases.json`](../../tests/qa_egress/cases.json) y en las pruebas
del mismo directorio.

| Escenario | Resultado observado |
|---|---|
| Solicitud permitida | Una llamada por solicitud con correo, RUT, CURP, RFC, CI boliviana, cédula colombiana, NIT boliviano y colombiano, tarjeta o teléfono enmascarados, según el caso. Se comprobaron intervalos exactos, JSON, listas y Unicode. |
| Casos negativos | El texto limpio y las referencias no sensibles llegaron intactos. |
| Rechazo, autenticación ausente y fallo de política | Cero llamadas al proveedor simulado antes del envío. |
| Timeout y streaming | Una llamada con el cuerpo enmascarado. El timeout se propagó sin reintento y el streaming entregó los dos fragmentos esperados. |
| Dos clientes ficticios | En tres solicitudes consecutivas A, B y A, cada respuesta correspondió al cuerpo recibido para esa llamada. |
| Evidencia | Los correos de prueba y los tokens no aparecieron en los logs capturados, la salida de pytest ni el JUnit local generado para esta comprobación. |

## Límites y dependencias

El endpoint público `/proxy/v1/chat` sigue devolviendo `503`. La integración
probada une componentes reales mediante un flujo definido exclusivamente en
las pruebas. La autenticación y los clientes son simulados, el timeout es una
excepción del transporte de prueba y el streaming usa fragmentos en memoria.
Estos resultados cubren el sandbox. La identidad, el aislamiento real, la
persistencia de auditoría y la sanitización obligatoria del proxy se verifican
por separado en [#7](https://github.com/andres-olguin/DELIA/issues/7),
[#8](https://github.com/andres-olguin/DELIA/issues/8) y
[#9](https://github.com/andres-olguin/DELIA/issues/9).

## Evidencia de registros y persistencia

El #55 comprueba una solicitud permitida y otra bloqueada mediante captura de
logs, stdout y stderr. La ejecución local también revisó el JUnit con captura
habilitada. Los correos originales y los tokens ficticios estuvieron ausentes
de esas salidas. El sandbox conserva las solicitudes simuladas en memoria.

El [issue #8](https://github.com/andres-olguin/DELIA/issues/8) sigue la
verificación de persistencia. Cuando exista una ruta de escritura disponible
para pruebas, usar una base desechable y ejecutar una solicitud permitida y
otra bloqueada con identificadores ficticios. Comprobar que el flujo ejerce
la escritura de auditoría, que se guardan solo los campos acordados y que
los prompts, respuestas y tokens originales están ausentes. Una tabla vacía
con la ruta deshabilitada no acredita ese comportamiento.

Queda por acordar con el responsable del #8 el destino de prueba y los campos
permitidos. La externalización de secretos y la evaluación de datos
históricos también se siguen en ese issue.
