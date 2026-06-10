# Storytelling + Fixes — TP3 Diseño Data-Centric

## Resumen Ejecutivo

La presentación tiene **discrepancias graves** entre las slides y los datos del notebook. El problema central: las slides cuentan una historia de mejora exitosa (Path A gana, F1 sube de 0.7185 a 0.7231), pero el notebook dice que **ninguna estrategia mejoró el baseline**. El modelo final es idéntico al baseline con F1=0.7185 y mejora +0.0000.

**Narrativa elegida:** Resultado negativo honesto — el análisis data-centric no mejoró el rendimiento global, pero reveló información valiosa sobre la heterogeneidad oculta del modelo y las limitaciones de las intervenciones sobre datos.

---

## Nuevo Orden de Slides

| # | Slide | Tipo | Estado |
|---|---|---|---|
| 01 | Portada | dark | ✅ Sin cambios |
| 02 | El Problema y el Dataset | light | ⚠️ Minor tweak |
| 03 | Sección NB01-02 | dark | ✅ Sin cambios |
| 04 | Notebook 01: Limpieza | white | ⚠️ Minor tweak |
| 05 | Notebook 02: Comparación de Modelos | light | ⚠️ Actualizar tabla con números tuned |
| 05b | **[NUEVA] Proceso de Selección: Tuning** | white | 🆕 Agregar |
| 06 | Baseline: XGBoost — Evaluación en Test | dark | ⚠️ Agregar confusion matrix |
| 07 | Sección NB03 | dark | ✅ Sin cambios |
| 08 | Análisis de Errores por Cohorte | white | ⚠️ Minor tweak |
| 08b | **[NUEVA] FPR vs FNR: No Todos los Errores Son Iguales** | light | 🆕 Agregar |
| 09 | Cohorte Problemática: internal_research | light | ✅ Sin cambios |
| 10 | Curvas de Aprendizaje — XGBoost | white | 🚨 Corregir conclusión |
| 11 | Tres Estrategias Data-Centric | light | ✅ Sin cambios |
| 12 | Comparación de Estrategias | white | 🚨 Reescribir completamente |
| 12b | **[NUEVA] ¿Por Qué Ninguna Estratégia Mejoró?** | white | 🆕 Agregar |
| 13 | Modelo Final | light | 🚨 Reescribir completamente |
| 14 | Conclusiones | dark | 🚨 Reescribir completamente |

---

## Detalle Slide por Slide

---

### SLIDE 01 — PORTADA ✅

**Sin cambios.**

Contenido actual:
- Pill: "72.75 Aprendizaje Automático — ITBA"
- Título: "Diseño Data-Centric"
- Subtítulo: "Predicción de Cancelación de Reservas GPU mediante Análisis de Errores por Cohorte y Estrategia de Datos"

---

### SLIDE 02 — EL PROBLEMA ⚠️ TWEAK MENOR

**Contenido actual:** Stats + objetivo + métricas.

**Fix menor:**
- El stat card "9.551 Reservas GPU" está bien.
- "29 Variables originales" → bien.
- "37% Tasa de cancelación" → aclarar que es del dataset completo (37.04%), no del train (37.6%) ni del test (34.6%).
- "80/20 Split temporal" → bien.
- Los bullets dicen "37% positivos (cancelados) en train, 34.6% en test" → correcto según el notebook (37.6% y 34.6%). **Cambiar "37%" a "37.6%"** en el bullet.

---

### SLIDE 03 — SECCIÓN NB01-02 ✅

**Sin cambios.**

---

### SLIDE 04 — NOTEBOOK 01: LIMPIEZA ⚠️ TWEAK MENOR

**Contenido actual:** 4 bullets (EDA, leakage, feature engineering, split temporal) + stat cards + highlight "55 features".

**Fixes:**
- Bullet de leakage: dice "total_gpu_hours, total_processes, request_month". Confirmado por notebook: ✅. La justificación en la slide no menciona que `request_month` se saca por correlación 0.995 con `request_week`. Podría agregar ese detalle.
- Bullet de feature engineering: dice "encoding cíclico de request_week (sin/cos) + OHE para categóricas". ✅ Correcto.
- Stat cards: Train 7.640, Test 1.911. ✅.
- "37.6% cancelados" y "34.6% cancelados" → ✅ Coincide con notebook.
- Highlight "55 features finales" → cambiar a incluir que se eliminaron 3 por leakage/redundancia. Ej: "55 features finales (3 eliminadas por leakage/redundancia, 2 creadas por encoding cíclico)".

---

### SLIDE 05 — NOTEBOOK 02: COMPARACIÓN DE MODELOS ⚠️ ACTUALIZAR TABLA

**Contenido actual:** Tabla con CV F1 y ROC-AUC de los 5 modelos.

**Fix:** La tabla actual muestra los números **tuned** para XGBoost pero mezcla con baseline para otros. Usar los números tuned correctos del notebook:

| Modelo | CV F1 | CV ROC-AUC |
|---|---|---|
| Naive Bayes | 0.614 | 0.769 |
| LDA | 0.636 | 0.831 |
| SVM (RBF) | 0.676 | 0.811 |
| Random Forest | 0.645 | 0.857 |
| **XGBoost ✓** | **0.698** | **0.860** |

**Nota:** Los números de la slide actual dicen 0.594, 0.636, 0.639, 0.677, 0.698 para F1 — son los valores **baseline** (antes de tuning), no los tuned. El notebook 02 muestra ambos. Decidir cuál mostrar:

- Opción A: Mostrar solo los tuned (0.614, 0.636, 0.676, 0.645, 0.698).son los relevantes para la selección.
- Opción B: Mostrar baseline vs tuned en dos columnas.

**Recomendación:** Mostrar tuned, porque son los que determinaron la selección. Pero XGBoost tuned pasa de 0.698 (mostrado como 0.698 en la slide) a 0.723 con tuned según el notebook. En la slide actual dice 0.698 — **esto es correcto como CV F1 tuned**.

Espera — rechecking: Los números de la slide actual (0.594, 0.636, 0.639, 0.677, 0.698) coinciden con los valores **baseline** del notebook para NB, LDA, SVM y RF, pero el de XGBoost (0.698) coincide con el baseline (0.6975 ≈ 0.698). Los valores tuned son: NB 0.614, LDA 0.636, SVM 0.676, RF 0.645, XGBoost 0.723.

**Decisión:** Usar los valores **tuned**, que son los finales después de hyperparameter optimization. Esto cambia la tabla significativamente (XGBoost pasa de 0.698 a 0.723, RF baja de 0.677 a 0.645):

| Modelo | CV F1 (tuned) | CV ROC-AUC (tuned) |
|---|---|---|
| Naive Bayes | 0.614 | 0.769 |
| LDA | 0.636 | 0.831 |
| SVM (RBF) | 0.676 | 0.811 |
| Random Forest | 0.645 | 0.857 |
| **XGBoost ✓** | **0.723** | **0.860** |

**También actualizar ROC-AUC:** la slide actual muestra 0.757, 0.831, 0.825, 0.850, 0.847 — estos son baseline. Los tuned son: 0.769, 0.831, 0.811, 0.857, 0.860.

**Label del slide:** Cambiar "CV F1 promedio (TimeSeriesSplit, 5 folds)" — es correcto.

---

### SLIDE 05b — [NUEVA] PROCESO DE SELECCIÓN: TUNING

**Tipo:** white

**Contenido:**
- Label: "Notebook 02 — Selección del Modelo"
- Heading: "De 5 Clasificadores al Baseline: Tuning y Overfitting"
- Layout: two-col
  - Izquierda: imagen `before_after_tuning.png` — muestra el impacto del tuning en F1 y AUC para los 5 modelos
  - Derecha: bullets o highlights
    - "XGBoost mejora de CV F1 0.698 a 0.723 con tuning de learning_rate, max_depth y n_estimators"
    - "Random Forest: tuning reduce overfitting (Train F1 1.0 → 0.685) pero no alcanza a XGBoost"
    - "El gap de overfitting de XGBoost (0.083) es manejable y menor que el de RF (0.323 baseline, 0.040 tuned)"

**Imagen a copiar:** `outputs/before_after_tuning.png` → `images/before_after_tuning.png`

**Opcionalmente agregar:** `outputs/overfitting_train_vs_cv.png` como segunda imagen o en lugar de la primera.

---

### SLIDE 06 — BASELINE XGBOOST ⚠️ AGREGAR CONFUSION MATRIX

**Contenido actual:** F1=0.7185 y AUC=0.8772 en números grandes. 3 stat cards: Pipeline, Tuning, Desbalance.

**Fixes:**
- Los números son correctos: F1=0.7185, AUC=0.8772 ✅
- Las 3 stat cards del fondo son genéricas. Propuesta de reemplazo:

**Opción A:** Reemplazar las 3 stat cards con una confusion matrix visual y dos stat cards específicas:
- CM: 1078 TN | 171 FP | 195 FN | 467 TP
- Stat card 1: "FPR Global = 13.7%" (171/1249)
- Stat card 2: "FNR Global = 29.4%" (195/662)

**Opción B:** Agregar la imagen `xgboost/confusion_matrix_test.png` en la sección inferior.

**Imagen a copiar:** `outputs/xgboost/confusion_matrix_test.png` → `images/confusion_matrix_baseline.png`

**Los números a mostrar:**
- F1-Score: 0.7185
- ROC-AUC: 0.8772
- Confusion matrix: TN=1078, FP=171, FN=195, TP=467
- Accuracy: 0.8085
- FPR: 13.7% | FNR: 29.4%

---

### SLIDE 07 — SECCIÓN NB03 ✅

**Sin cambios.**

---

### SLIDE 08 — ANÁLISIS DE ERRORES POR COHORTE ⚠️ TWEAK MENOR

**Contenido actual:** Gráfico + 3 bullets + highlight box.

**Fixes:**
- Bullet "client_type: alta heterogeneidad. Rango F1: 0.0 → 0.87" → El valor exacto es 0.8693. "0 a 0.87" está bien como redondeo. ✅
- Bullet "service_tier: enterprise mejor (F1=0.92)" → El valor exacto es 0.9167. Cambiar a "F1=0.917" para ser más preciso, o dejar 0.92 como redondeo.
- Bullet "reserved_gpu_type: GPU_T5, T7, T4 con F1 < 0.60" → GPU_T5=0.4737, T7=0.5000, T4=0.5714. ✅
- Highlight box: "F1=0.72" → El global es 0.7185. Cambiar a "F1≈0.72" o "F1=0.72". ✅
- **Agregar segundo insight al highlight box:** "No solo hay variación en F1: algunas cohortes fallan por no detectar cancelaciones (FNR alto), otras por falsas alarmas (FPR alto)."

---

### SLIDE 08b — [NUEVA] FPR vs FNR: NO TODOS LOS ERRORES SON IGUALES

**Tipo:** light

**Contenido:**
- Label: "Sección 3.1 — Profundización"
- Heading: "No Todos los Errores Son Iguales"
- Layout: two-col
  - Izquierda: Tabla o gráfico simplificado mostrando FPR y FNR por cohorte (client_type):
    - internal_research: FNR=72.7% (casi 3 de cada 4 cancelaciones no detectadas)
    - enterprise_client: FNR=76.5%
    - cloud_marketplace: FPR=21.4% (muchas falsas alarmas)
    - research_consortium: FPR=17.3% + FNR=14.4%
    - managed_account: FPR=3.9% + FNR=23.5%
  - Derecha: Highlight box con conclusión
    - "Las cohortes no solo difieren en F1, sino en el **tipo** de error"
    - "internal_research y enterprise_client: FNR muy alto → el modelo no detecta cancelaciones reales"
    - "cloud_marketplace: FPR alto → el modelo marca demasiados falsos positivos"
    - "Esto sugiere que necesitaríamos estrategias diferentes por cohorte"

**Datos para la tabla (client_type, test set):**

| Cohorte | n | F1 | FPR | FNR |
|---|---|---|---|---|
| high_priority_partner | 4 | 0.000 | 0.000 | 1.000 |
| sponsored_project | 20 | 0.000 | 0.105 | 1.000 |
| enterprise_client | 119 | 0.286 | 0.069 | 0.765 |
| **internal_research** | **183** | **0.308** | **0.068** | **0.727** |
| cloud_marketplace | 804 | 0.599 | 0.214 | 0.377 |
| managed_account | 446 | 0.835 | 0.039 | 0.235 |
| research_consortium | 335 | 0.869 | 0.173 | 0.144 |

---

### SLIDE 09 — COHORTE PROBLEMÁTICA: INTERNAL_RESEARCH ✅

**Sin cambios.** Los números coinciden con el notebook:
- F1=0.31 (exacto: 0.3077) ✅
- FNR=73% (exacto: 0.7273) ✅
- 10.6% del dataset ✅
- 1.009 instancias ✅
- 826 instancias en train ✅
- 15.4% tasa de cancelación (exacto: 15.36%) ✅
- Estacionalidad: Ene-Feb 8%, May-Jun 21%, Jul-Ago 22% ✅

---

### SLIDE 10 — CURVAS DE APRENDIZAJE 🚨 CORREGIR CONCLUSIÓN

**Contenido actual:** Gráfico + 3 bullets + highlight box que dice "El sistema es data-limited" y "Agregar datos reales tiene potencial de mejora".

**Fix CRÍTICO:** El notebook dice que el diagnóstico principal es **"Alto overfitting"** (gap=0.1529 > 0.15), no solo "data-limited". La curva CV sí sube (mejora 0.0382 de 50% a 100%), pero el gap indica que la mayor parte de la mejora pasa por regularización, no solo datos.

**Nuevos bullets:**
1. "Gap train/CV = 0.15 → **overfitting moderado**. El modelo memoriza patrones del train que no generalizan."
2. "La curva CV sigue creciendo al agregar datos → más datos **podría** ayudar, pero no es la única solución."
3. "Conclusión: el sistema es **AMBOS** — overfitea Y necesita más datos de las cohortes débiles."

**Nuevo highlight box:**
- Título: "Diagnóstico dual"
- "El modelo overfitea (gap=0.15) pero la curva CV es ascendente. Agregar datos de las cohortes débiles podría ayudar, PERO solo si esos datos tienen señal — de lo contrario, amplifica el overfitting."

---

### SLIDE 11 — TRES ESTRATEGIAS DATA-CENTRIC ✅

**Sin cambios.** Las cards son correctas:
- Path A: +500 instancias reales, cancel_rate extra 18.2% ✅
- Path B: +560 instancias sintéticas (SMOTE) ✅
- Path C: Pesos ×3.0 ✅

**Minor:** La card de Path A dice "Train: 7.640 → 8.140". Confirmado ✅.
La card de Path B dice "Train: 7.640 → 8.200". Confirmado ✅.
La card de Path C dice "Train size: sin cambio". Confirmado ✅.

---

### SLIDE 12 — COMPARACIÓN DE ESTRATEGIAS 🚨 REESCRIBIR COMPLETAMENTE

**Contenido actual (INCORRECTO):** Muestra F1 de test: Baseline 0.7185, Path A 0.7231 (+0.0046), Path C 0.7209 (+0.0024), Path B 0.7115 (−0.0070). Estos números NO EXISTEN en el notebook.

**Reemplazar con evaluación CV (los únicos números con respaldo):**

| Estrategia | CV F1 | CV AUC | Δ F1 vs Baseline |
|---|---|---|---|
| **Baseline** | **0.7228 ± 0.022** | **0.8604 ± 0.021** | — |
| Path A (datos reales) | 0.6993 ± 0.021 | 0.8561 ± 0.011 | −0.024 ↓ |
| Path C (class weight) | 0.7198 ± 0.030 | 0.8581 ± 0.024 | −0.003 ↓ |
| Path B (SMOTE) | 0.7171 ± 0.046 | 0.8591 ± 0.023 | −0.006 ↓ |

**Narrativa nueva:**

Compare rows:
- Baseline: 0.7228 (ganador)
- Path A — Datos Reales: 0.6993 (−0.024) — empeora
- Path C — Class Weight: 0.7198 (−0.003) — casi igual
- Path B — SMOTE: 0.7171 (−0.006) — empeora

**Highlight box nuevo:**
- Título: "Resultado inesperado: ninguna estrategia mejora"
- Contenido: "Agregar 500 instancias reales de internal_research empeora el F1 global (−0.024). Esto se debe a que la señal de cancelación en esa cohorte (16.1%) es más débil que la del dataset completo (37.6%). Las instancias extras 'diluyen' la señal en lugar de reforzarla."

**Imagen:** `images/real_vs_smote_comparison.png` — verificar que los números coincidan con CV. Si la imagen muestra los números antiguos (test), habrá que regenerarla.

---

### SLIDE 12b — [NUEVA] ¿POR QUÉ NINGUNA ESTRATEGIA MEJORÓ?

**Tipo:** light

**Contenido:**
- Label: "Análisis post-hoc"
- Heading: "¿Por Qué Ninguna Estratégia Mejoró el F1 Global?"
- Layout: three-col o two-col

**Izquierda — Razones:**
1. **Path A (datos reales) empeora:** Los 500 datos extra tienen cancel_rate=18.2%, mucho menor que el global (37.6%). Agregarlos diluye la señal — el modelo aprende de datos con menos positivos.
2. **SMOTE genera artefactos:** En internal_research, la clase positiva es internamente heterogénea (cancelaciones varían estacionalmente de 8% a 22%). Interpolar entre cancelaciones de meses distintos crea instancias irreales.
3. **Class Weight ×3 es insuficiente:** Triplicar el peso de 826 instancias (10.8% del train) no compensa su baja tasa de cancelación (16.1%) ni su patrón diferente.

**Derecha — SMOTE por cohorte (análisis diagnóstico):**

Tabla de F1 por cohorte (client_type), baseline vs SMOTE:

| Cohorte | F1 baseline | F1 SMOTE | Δ |
|---|---|---|---|
| enterprise_client | 0.286 | 0.333 | +0.048 |
| managed_account | 0.835 | 0.845 | +0.010 |
| cloud_marketplace | 0.599 | 0.607 | +0.007 |
| research_consortium | 0.869 | 0.876 | +0.007 |
| **internal_research** | **0.308** | **0.282** | **−0.026** |

Conclusión: "SMOTE empeora la cohorte específica que queremos ayudar."

---

### SLIDE 13 — MODELO FINAL 🚨 REESCRIBIR COMPLETAMENTE

**Contenido actual (INCORRECTO):** F1=0.7231 (+0.0046), AUC=0.8827 (+0.0055), CM 1067/182/184/478.

**Reemplazar con:**

- Título: "Modelo Final = Baseline XGBoost"
- Subtítulo: "Ninguna intervención data-centric superó el baseline global"
- Métricas correctas:

| Métrica | Valor | vs Baseline |
|---|---|---|
| F1-Score | 0.7185 | +0.0000 |
| ROC-AUC | 0.8772 | +0.0000 |

- Stat cards:
  - Pipeline: StandardScaler → XGBoost (no cambios)
  - Train size: 7.640 instancias (sin datos adicionales)
  - Features: 55 (sin cambios)

- Confusion matrix correcta: TN=1078, FP=171, FN=195, TP=467
- Precision=0.732, Recall=0.706

**Highlight box:**
- "El modelo elegido por CV es el baseline sin modificaciones. Esto no es un fracaso del enfoque data-centric — es un hallazgo: el cuello de botella no es la cantidad de datos de internal_research, sino la calidad de la señal en esa cohorte."

**Imagen:** Regenerar `final_model_evaluation.png` para que muestre F1=0.718 y AUC=0.88, no 0.723 y 0.883.

---

### SLIDE 14 — CONCLUSIONES 🚨 REESCRIBIR COMPLETAMENTE

**Contenido actual (INCORRECTO):** Bullets que dicen "Los datos reales superan a SMOTE" y "El diseño data-centric mejora el F1 de 0.7185 a 0.7231".

**Reemplazar con nueva narrativa (dos columnas):**

**Columna izquierda — Hallazgos:**
1. **XGBoost** es el mejor clasificador baseline (CV F1=0.723, Test F1=0.718, ROC-AUC=0.877)
2. El análisis por cohortes revela **heterogeneidad oculta**: F1 varía de 0 a 0.87 según el tipo de cliente
3. **internal_research**: F1=0.31, FNR=73% — el modelo no detecta 3 de cada 4 cancelaciones reales
4. La curva de aprendizaje muestra **overfitting moderado** (gap=0.15) y potencial de mejora con más datos

**Columna derecha — Lecciones:**
5. **Ninguna intervención data-centric mejoró el F1 global** — el baseline ya era robusto para el promedio
6. Los datos reales extras empeoran (-0.024 F1) porque diluyen la señal: cancel_rate 18% vs 37% global
7. SMOTE empeora específicamente internal_research (-0.026 F1 en la cohorte)
8. **Un resultado negativo es valioso**: el problema no es cantidad de datos sino calidad de señal y representación

**Opcional — tercera sección pequeña:**
- Futuras direcciones: feature engineering específico por cohorte, modelos especializados (ensemble), threshold optimization por cohorte basado en costo operacional

---

## Imágenes que hay que copiar/regenerar

### Copiar de outputs/ a images/

| Archivo origen | Archivo destino | Slide |
|---|---|---|
| `outputs/before_after_tuning.png` | `images/before_after_tuning.png` | 05b |
| `outputs/overfitting_train_vs_cv.png` | `images/overfitting_train_vs_cv.png` | 05b |
| `outputs/xgboost/confusion_matrix_test.png` | `images/confusion_matrix_baseline.png` | 06 |
| `outputs/test_comparison.png` | `images/test_comparison.png` | 05 (opcional) |

### Imágenes que hay que regenerar

| Archivo | Motivo | Contenido esperado |
|---|---|---|
| `images/real_vs_smote_comparison.png` | Los números pueden ser de la versión antigua. Verificar que coincide con CV. | 4 estrategias con CV F1: Baseline 0.723, Path A 0.699, Path C 0.720, Path B 0.717 |
| `images/final_model_evaluation.png` | Muestra F1=0.72, AUC=0.88. La CM debe mostrar 1078/171/195/467. | F1=0.718, AUC=0.877, CM con TN=1078, FP=171, FN=195, TP=467 |

---

## Números de Referencia (del notebook, verificables)

### Baseline XGBoost — Test

| Métrica | Valor |
|---|---|
| F1-Score | 0.7185 |
| ROC-AUC | 0.8772 |
| Accuracy | 0.8085 |
| FPR | 13.69% (171/1249) |
| FNR | 29.39% (195/662) |
| TN | 1078 |
| FP | 171 |
| FN | 195 |
| TP | 467 |

### Baseline XGBoost — CV (TimeSeriesSplit 5-fold)

| Métrica | Valor |
|---|---|
| CV F1 | 0.7228 ± 0.0222 |
| CV ROC-AUC | 0.8604 ± 0.0214 |

### Estrategias — CV (TimeSeriesSplit 5-fold)

| Estrategia | CV F1 | CV F1 std | CV AUC | CV AUC std |
|---|---|---|---|---|
| Baseline | 0.7228 | 0.0222 | 0.8604 | 0.0214 |
| Path A (+500 reales) | 0.6993 | 0.0211 | 0.8561 | 0.0108 |
| Path C (weight ×3) | 0.7198 | 0.0304 | 0.8581 | 0.0241 |
| Path B (SMOTE +560) | 0.7171 | 0.0459 | 0.8591 | 0.0225 |

### Modelos Tuned — CV

| Modelo | CV F1 | CV AUC |
|---|---|---|
| Naive Bayes | 0.6144 | 0.7691 |
| LDA | 0.6356 | 0.8312 |
| SVM (RBF) | 0.6756 | 0.8111 |
| Random Forest | 0.6451 | 0.8570 |
| XGBoost | 0.7228 | 0.8604 |

### Modelos — Test

| Modelo | Test F1 | Test AUC | Test Acc |
|---|---|---|---|
| Naive Bayes | 0.6169 | 0.8083 | 0.6536 |
| LDA | 0.6311 | 0.8296 | 0.8048 |
| SVM (RBF) | 0.7058 | 0.8554 | 0.8216 |
| Random Forest | 0.6539 | 0.8691 | 0.8200 |
| XGBoost | 0.7185 | 0.8772 | 0.8085 |

### Cohorte internal_research (test)

| Métrica | Valor |
|---|---|
| n | 183 |
| cancel_rate | 12.0% |
| F1 | 0.3077 |
| FNR | 72.73% |
| FPR | 6.83% |
| TP | 6 |
| FP | 11 |
| FN | 16 |
| TN | 150 |

### Learning Curve

| Métrica | Valor |
|---|---|
| Gap train/CV (100% data) | 0.1529 |
| Val improvement (50% → 100%) | 0.0382 |
| Diagnóstico | Alto overfitting + data-limited |

### SMOTE vs Baseline por cohorte (client_type, diagnóstico)

| Cohorte | F1 baseline | F1 SMOTE | Δ |
|---|---|---|---|
| enterprise_client | 0.2857 | 0.3333 | +0.048 |
| managed_account | 0.8350 | 0.8454 | +0.010 |
| cloud_marketplace | 0.5993 | 0.6066 | +0.007 |
| research_consortium | 0.8693 | 0.8762 | +0.007 |
| high_priority_partner | 0.0000 | 0.0000 | 0.000 |
| sponsored_project | 0.0000 | 0.0000 | 0.000 |
| **internal_research** | **0.3077** | **0.2821** | **−0.026** |

---

## Resumen de Cambios por Prioridad

| Prioridad | Slide | Cambio |
|---|---|---|
| 🚨 CRÍTICO | 12 | Reescribir números y narrativa. Baseline gana, no Path A. |
| 🚨 CRÍTICO | 13 | Reescribir métricas. F1=0.7185, AUC=0.8772, mejora=0.0000. |
| 🚨 CRÍTICO | 14 | Reescribir conclusiones. Resultado negativo honesto. |
| ⚠️ ALTO | 10 | Corregir conclusión de learning curves. Es overfitting + data-limited, no solo data-limited. |
| ⚠️ ALTO | 05 | Actualizar tabla con números tuned (no baseline). |
| 🆕 NUEVA | 05b | Slide de tuning y selección del modelo. |
| 🆕 NUEVA | 08b | Slide de FPR vs FNR por cohorte. |
| 🆕 NUEVA | 12b | Slide "Por qué ninguna estrategia mejoró". |
| ⚠️ MEDIO | 06 | Agregar confusion matrix del baseline. |
| ⚠️ MENOR | 02 | Cambiar "37%" a "37.6%" en train. |
| ⚠️ MENOR | 04 | Ampliar highlight de leakage. |
| ⚠️ MENOR | 08 | Agregar insight sobre tipo de error (FPR vs FNR). |