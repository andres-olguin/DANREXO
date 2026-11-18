# DANREXO

**D**efensa de **A**gentes, **N**eutralización de **R**iesgos y **E**jecución e**X**plicable con **O**bservabilidad.

> **Controlar lo que los agentes pueden hacer, proteger lo que procesan y comprobar lo que realmente hicieron.**
>
> La expansión DANREXO es una **declaración de misión y posicionamiento**, no una certificación ni la afirmación de que estas capacidades ya funcionen en producción. La palabra **eXplicable** resalta la X de forma deliberada. Ver [fundamento de identidad](docs/branding/DANREXO_SIGNIFICADO_Y_NARRATIVA.md).

**Estado al 18/11/2026:** investigación y desarrollo con pruebas sintéticas. **No apto para datos reales de clientes, pasarela de seguridad productiva ni SaaS abierto al público.** Las verificaciones de seguridad y la revisión humana son obligatorias; los 8 controles críticos SEC-001…SEC-008 figuran abiertos en el [registro de preparación](docs/foundation/readiness-controls.json).

**Importante sobre el nombre:** DANREXO es el nombre comercial **elegido**, pero no consta como marca registrada ni libre de conflicto en todas las jurisdicciones. La migración pública/técnica sigue sujeta al [plan #54](https://github.com/andres-olguin/DELIA/issues/54). El repositorio continúa llamándose `DELIA` y conserva el historial **TALIA → DELIA → DANREXO**. No renombrar automáticamente imports, contratos API, rutas, GitHub Pages o base de datos.

## Qué problema buscamos resolver

Las organizaciones conectan agentes de IA con CRM, ticketing y herramientas que pueden manejar datos personales o ejecutar cambios. DANREXO investiga un enfoque de **aseguramiento operacional por proceso** que pretende integrar:

1. **Decisión previa:** determinar quién autoriza una acción y con qué alcance.
2. **Prevención de exposición:** minimizar datos sensibles antes de la comunicación externa.
3. **Ejecución controlada:** comprobar que una operación denegada no produce efectos.
4. **Evidencia de resultado:** distinguir una respuesta declarada de un cambio observado en una fuente independiente.
5. **Portabilidad:** repetir verificaciones entre integradoras y clientes, midiendo costo y esfuerzo.

**Lo que sí existe:** detector regional experimental de PII, suites de pruebas y benchmarks sintéticos, laboratorios de contratos y comparadores ficticios, documentación de riesgos y un frontend estático de demostración. **Lo que aún no está demostrado:** control de egreso integrado al proxy productivo, autenticación y aislamiento real por cliente, aprobación/revocación durable, verificación E2E de herramientas ni eficacia superior a competidores en infraestructura real. El endpoint proxy continúa bloqueado con HTTP 503 por diseño.

## Lectura rápida

| Necesidad | Documento |
|---|---|
| Estado técnico, límites y prioridades P0 | [Foundation — comenzar aquí](docs/foundation/README.md) |
| Controles verificables y criterios de salida | [13 controles y gates](docs/foundation/readiness-controls.json) |
| Riesgos técnicos detectados en el repositorio | [Auditoría de estructura 18/11/2026](docs/auditorias/AUDITORIA_ESTRUCTURA_DANREXO_2026-11-18.md) |
| Arquitectura y criterios de producto | [Tesis única y kill rules](docs/foundation/UNICA_APUESTA_Y_KILL_RULES.md) |
| Diferenciación aún por comprobar | [Laboratorio de contratos](docs/competitive-assurance/README.md) |
| Benchmark PII y sus límites | [Benchmarks](benchmarks/README.md) |
| Primera oferta comercial hipotética | [Servicio de diagnóstico](docs/foundation/SERVICIO_DIAGNOSTICO.md) |
| Desarrollo del frontend sintético | [Sitio estático](site/README.md) |
| Identidad comercial / riesgos de marca | [Decisión DANREXO](docs/branding/DANREXO_DECISION_Y_SPRINT3.md) |
| Índice por vigencia y tema | [Mapa de documentación](docs/README.md) |
| Contenido del README anterior (histórico) | [Archivo legado](docs/archive/README_DELIA_HISTORICO_2026-11-18.md) |

## Estructura del repositorio

```text
app/, services/, models/   API experimental y esquemas (NO producción)
backend/                   DLP regional, logs y utilidades
tests/, benchmarks/         Regresión y evaluación sintética
experiments/                Laboratorios de verificación de resultados
competitive_assurance/      Comparación con adaptadores ficticios
commercial_ops/             Simuladores comerciales; no ventas acreditadas
site/                       Página y demostraciones estáticas, sin backend
tools/                      Validación y diagnóstico local
docs/                       Documentación por tema, vigencia y archivo
.github/workflows/          Automatización de CI y publicación de site/
.agents/skills/             Recursos de agentes; inventario pendiente de depuración
```

## Comprobar el estado localmente

Usa un entorno aislado y **solo datos sintéticos**; no introduzcas tokens ni credenciales de proveedores:

```bash
python -m pip install -r requirements-test.txt
python -m pip check
python -m pytest -q --tb=short tests/
python -m tools.foundation_doctor
```

Para Python 3.11 y 3.13, seguir `requirements-test-compat.txt`; CI contiene una matriz de compatibilidad. El comando `python -m tools.foundation_doctor --require-production-ready` **debe rechazar** el release mientras falte evidencia. Un CI verde no autoriza activar el proxy.

Para probar la web de demostración: `node tools/check-public-site.mjs` y [verificar su alcance](site/README.md).

## Colaboración y límites

- [Contribución](CONTRIBUTING.md), [seguridad y divulgación privada](SECURITY.md), [issues abiertos](https://github.com/andres-olguin/DELIA/issues) y [PR pendientes](https://github.com/andres-olguin/DELIA/pulls).
- Trabajar en ramas/PR con pruebas, revisión humana y registro de límites; no modificar automáticamente un PR de otra persona ni borrar historia.
- No incluir datos personales reales, claves, logs privados ni documentos internos. Los experimentos no deben reclamar certificaciones, rendimientos poblacionales, clientes, ventas o superioridad competitiva sin pruebas.
- La línea comercial inmediata es un **diagnóstico profesional sujeto a alcance, contrato y capacidad**, no una licencia de gateway ni una promesa de protección productiva.

**Mantenedor:** dirección del repositorio. **Licencia:** [MIT](LICENSE). Las marcas y los derechos de terceros se evalúan por separado.
