# Auditoría estructural de DANREXO — 18/11/2026

**Tipo:** análisis estático de árbol Git, navegación y archivos de muestra. **Objeto:** repositorio `andres-olguin/DELIA`, rama `main` observada antes de las ediciones, árbol `f48273c19650128028d487bcfbe8f1daf957bdae`. **No ejecuta** pentest, CI independiente, escáner de secretos ni pruebas de producción; no atribuir a esta auditoría certificación, limpieza definitiva o release autorizado.

## 1. Inventario reproducible de Git

| Área | Archivos Git | Tamaño del contenido según objetos Git |
|---|---:|---:|
| Total | **304 archivos**, 60 directorios | — |
| `docs/` | **152** | **1.407.467 B** |
| `.agents/` | **51** | **509.479 B** |
| `benchmarks/` | **16** | **229.112 B** |
| `tests/` | **21** | **67.726 B** |
| `site/` | **5** | **37.917 B** |
| `.github/workflows/` | **11** | **16.506 B** |
| `README.md` | 1 | **56.935 B** |

La estructura es amplia para el producto experimental. La cantidad de documentos no equivale a cobertura, funcionalidad ni aprobación. El árbol no mostró patrones obvios de archivos `.pyc`, `__pycache__`, `.env` real, `node_modules` o `.bak` versionados; esto **no** sustituye análisis de todos los contenidos o del historial de Git.

## 2. Hallazgos priorizados: qué sobra, se duplica o crea riesgo

| ID | Prioridad | Evidencia concreta | Dictamen | Acción |
|---|---|---|---|---|
| HYG-01 | **P1** | README de 56.935 B mezcla 2026-10-31, Sprint 2, varios programas de crecimiento, benchmarks históricos y propuestas 2027, antes de llegar al producto | **Deuda de navegación y vigencia**; confunde decisión actual con histórico | **Aplicado en este PR:** README corto y archivo legado legible, sin borrar evidencia |
| HYG-02 | **P1** | `.gitignore` contiene `/site` aunque `site/` tiene 5 archivos y Pages despliega desde allí | **Riesgo de ignorar archivos nuevos** del frontend; los ya rastreados permanecen | **Aplicado en este PR:** sustituir regla por `/_site/` con explicación; verificar `git check-ignore` localmente |
| HYG-03 | **P1** | `docs/roadmap.md` mantiene cargos/asignaciones históricas, incluidos Nilson y un COO declarado, y stack planificado; además fechas antiguas | **No es fuente vigente de personal ni estado técnico** | Marcar como histórico en el índice, actualizar página solo con nueva acta validada; no borrar autoría ni alterar contratos |
| HYG-04 | **P2** | `docs/DELIA_viabilidad_mercado_regulatoria.md` y `research/TALIA en Colombia y Chile_ viabilidad de mercado y regulatoria (octubre de 2026).md` tienen contenido **exactamente igual tras normalizar TALIA/DELIA y quitar salto de línea final** | **Copia de rebranding, redundante**; ambas pueden sostener links históricos | Mantener por ahora; elegir canónica, inventariar referencias, documentar alias y solo entonces archivar/quitar duplicación |
| HYG-05 | **P2** | 51 archivos bajo `.agents/skills/` (509.479 B): múltiples guías genéricas de diseño web, imagen, animaciones y variantes `design-taste-frontend(-v1)`, `transitions-dev` | **Posible dependencia/volumen innecesario**, NO desuso demostrado | Revisar procedencia, licencias, llamadas de agentes y utilidades; conservar exclusivamente habilidades verificadas mediante PR y pruebas, antes de eliminar |
| HYG-06 | **P2** | 152 archivos en `docs/`, incluyendo 20 guías `docs/commercial-master`, varias versiones `docs/ventas`, matrices y materiales de marketing sin ventas probadas | **Exceso de material frente a la ejecución**; no necesariamente basura | Índice activo/experimental/histórico; desduplicar planes sin perder fuente ni bibliografía; no comercializar borradores como resultados |
| HYG-07 | **P2** | `docs/PROSPECTOS_RONDA2_160_CL_CO_MX_BO_2026-10-31.csv` (154.798 B) y `docs/ventas/SECUENCIAS_CONTACTO_4_PASOS.md` (67.880 B) | **Material comercial voluminoso y posiblemente obsoleto**; no confirma interesados ni cumplimiento | Revisar procedencia, consentimiento, vigencia, exactitud y privacidad; conservar evidencia histórica; excluir de mensajes de marketing automáticos |
| HYG-08 | **P1** | 11 workflows; algunos validan corpus/documentos comerciales, mientras `python-tests.yml` y `public-site-pages.yml` cumplen otro propósito | **Dispersión operativa**; no se comprobó duplicación funcional de jobs | Construir matriz workflow→paths→tiempo/costo→dueño; consolidar solo tras verificar equivalencia, condiciones de protección y resultados |
| HYG-09 | **P1** | `app/`, `backend/`, `services/`, `models/` combinan capas de red y negocio con pruebas y rutas distintas; P0 de proxy/auth/DB abiertos | **Deuda de límites y ownership**; no justifican refactor masivo ahora | Definir diagrama de paquetes, imports, DTO y fronteras de seguridad; **no mover** código sin PR propios y tests de import/integración |
| HYG-10 | **P2** | `SECURITY.md` y `CONTRIBUTING.md` usan dirección de contacto `contacto@mastertechg.com`; otras propiedades corporativas pueden tener contacto distinto | **Verificación de canal pendiente**; no afirmar rotura sin prueba de entrega | Confirmar buzón monitoreado, cambiar simultáneamente con validación y mantener divulgación privada |
| HYG-11 | **P2** | `benchmarks/resultados_*.json` y corpus `synthetic_pii_*.jsonl` acumulados por rondas | Son **artefactos de evidencia**, no basura probada | Establecer manifiesto de versiones/hash, baseline y retención; no borrar resultados que soportan afirmaciones |
| HYG-12 | **P2** | `README.md` y otras guías usan DELIA/TALIA, y algunos mensajes/metadata de Pages también | Migración **técnica no autorizada** hasta revisar la marca y compatibilidad | Mantener historia TALIA→DELIA→DANREXO, migración por capas mediante #5/#54/#56 |

### Archivos idénticos según SHA

La única coincidencia exacta de blob encontrada por SHA corresponde a cuatro archivos `__init__.py` vacíos (`app/`, `backend/`, `backend/data_access/`, `backend/dlp/`). **No son basura:** son marcadores de paquetes de Python; no eliminarlos.

### Limitaciones del inventario

Se verificó el árbol Git completo sin truncamiento, rutas, tamaños y archivos concretos como README, `.gitignore`, páginas clave de documentación, CI y archivos de viabilidad. No se inspeccionó el contenido de los 304 archivos línea por línea ni se comprobó si existen secretos en commits históricos, licencias de cada skill o dependencias externas de cada archivo. La clasificación de *candidato* no equivale a autorización para borrar.

## 3. Reorganización segura aplicada

1. Raíz: README reducido a identidad, estado, propuesta de valor, navegación, pruebas y riesgos reales; sin prometer ventas ni seguridad productiva.
2. `docs/archive/README_DELIA_HISTORICO_2026-11-18.md`: conservar el README anterior de forma legible, con enlaces Markdown relativos ajustados tras el cambio de ubicación.
3. `docs/README.md`: índice por fuente de verdad vigente, ingeniería/QA, investigación y archivo.
4. `docs/branding/DANREXO_SIGNIFICADO_Y_NARRATIVA.md`: expansión y mensajes editoriales; trazabilidad de condición de marca no registrada.
5. `.gitignore`: corregir exclusión incorrecta del frontend manteniendo exclusión de salida de generador.

**No modificados:** API, DB, tests, workflows, código de detector, CSV, materiales de investigación, PR abiertos de colaboradores, modelos de venta ni permisos. **No se han borrado** archivos históricos de terceros.

## 4. Backlog para depuración posterior

- **P1, seguridad:** resolver controles SEC-001…SEC-008 de [foundation](../foundation/readiness-controls.json). No confundir documentación con protección.
- **P1, compatibilidad frontend:** `git check-ignore -v site/nuevo-asset.svg` debe dejar de devolver `.gitignore:...` por la regla obsoleta; ejecutar CI Pages y prueba real sobre rama antes de publicar.
- **P1, arquitectura:** mapa de dependencias e imports y dueño único para políticas de salida, identidad, auditoría y readback.
- **P2, revisión de agentes:** relacionar cada una de las 51 skills con agente/uso/licencia; marcar `KEEP`, `MERGE` o `REMOVE_AFTER_TEST`; eliminar solo en PR exclusivo y con aprobación.
- **P2, fuentes comerciales:** designar documentos canónicos por tema y dejar histórico referenciable; revisar CSV de prospectos sin tratarlo como CRM validado.
- **P2, automatización:** inventario de 11 workflows, su costo y criticidad; eliminar solo checks redundantes tras pruebas de equivalencia.
- **P2, calidad editorial:** añadir un validador automático de enlaces relativos y evitar enlaces rotos durante futuras migraciones.
- **P2, actualización de sprints:** quitar cualquier presentación de roles, promesas o plazos históricos como estado vigente. No reescribir actas ni autoría.
- **P2, release truth:** verificar CI sobre SHA integrado, reportes, cobertura medida, QA independiente y permisos de producción antes de modificar flags de seguridad.

## 5. Reglas para eliminar archivos

Un borrado debe demostrar **(a)** ausencia de imports/enlaces/consumidores, **(b)** respaldo de la fuente única y autoría, **(c)** prueba relevante antes/después, **(d)** PR reversible revisado y **(e)** impacto aceptado en CI, Pages y colaboradores. Si alguno falta, archivar o conservar. No hacer `git clean` o purgas masivas.

**Dictamen:** el mayor problema visible no es un archivo temporal sino **fragmentación documental, antigüedad de instrucciones y dispersión de trabajo**. Esta PR resuelve la primera capa sin tocar componentes críticos; la segunda fase es racionalizar skills, planes y flujos por valor medido, no por conteo de archivos.
