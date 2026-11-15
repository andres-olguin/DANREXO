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

El commit de pruebas `b9bb3d7` obtuvo **27 casos aprobados** con las variables de
credenciales retiradas y las operaciones de red bloqueadas mediante un hook de
auditoría de Python. Los datos están en
[`tests/qa_egress/cases.json`](../../tests/qa_egress/cases.json) y en las pruebas
del mismo directorio.

| Escenario | Resultado observado |
|---|---|
| Solicitud permitida | Una llamada por solicitud con correo, RUT, CURP, CI boliviana o cédula colombiana enmascarados, según el caso. Se comprobaron JSON, listas y Unicode. |
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
