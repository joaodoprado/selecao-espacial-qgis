# 🗺️ Spatial Isolation Detector

[![QGIS](https://img.shields.io/badge/QGIS-3.22+-green.svg)](https://qgis.org)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Algoritmo de processamento customizado para o **framework QGIS Processing** que automatiza a identificação de **feições pontuais isoladas** utilizando **Spatial Index (R-Tree)** e cálculos geodésicos precisos.

A ferramenta foi desenvolvida para otimizar workflows de análise espacial, automatizando uma tarefa que normalmente exige inspeção manual em grandes datasets geoespaciais.

---

## 📸 Interface da Ferramenta

<img src="/docs/IMAGENS/interface_tool.png" alt="Interface da ferramenta no QGIS" width="776">

---

## 📌 Como Usar

1. Baixe o arquivo `selecao_pontos_isolados.py`
2. No QGIS abra:

Processamento → Caixa de Ferramentas → Scripts → Adicionar Script ao Painel

3. Selecione o arquivo do script
4. Execute a ferramenta em:

Scripts → Seleção de Pontos Isolados (Métrico)

---

## ⚙️ Como o Algoritmo Funciona

1. Criação de um **Spatial Index (R-Tree)** da camada de referência
2. Iteração sobre cada ponto da camada analisada
3. Consulta espacial usando **bounding box** no índice
4. Cálculo de distância geodésica com **QgsDistanceArea**
5. Caso nenhuma feição esteja dentro do raio definido → o ponto é classificado como **isolado**
6. O resultado é gravado em uma nova camada de saída

Essa abordagem reduz drasticamente o número de comparações espaciais necessárias em datasets grandes.

---

## 🚀 Diferenciais Técnicos

| Recurso                       | Benefício                                                |
| ----------------------------- | -------------------------------------------------------- |
| **Spatial Index (R-Tree)**    | Redução da complexidade de **O(n²)** para **O(n log n)** |
| **QgsDistanceArea**           | Cálculo geodésico elipsoidal com alta precisão           |
| **Case-insensitive matching** | Maior robustez em datasets heterogêneos                  |
| **Saída padronizada**         | Facilita integração com pipelines de dados               |

---

## ⚡ Performance

Benchmark aproximado em dataset real:

* **50.000 pontos:** ~5 segundos de processamento
* **Complexidade:** O(n log n)
* **Precisão:** cálculo geodésico elipsoidal

Os ganhos de performance vêm principalmente da utilização de **indexação espacial (R-Tree)** para reduzir o número de consultas de distância.

---

## 🛠️ Stack Tecnológico

* **PyQGIS** — API Python do QGIS
* **QGIS Processing Framework** — integração com toolbox nativa
* **Spatial Index (R-Tree)** — consultas espaciais otimizadas
* **QgsDistanceArea** — cálculos geodésicos elipsoidais

---

## 🎯 Motivação

Em diversos fluxos de trabalho de geoprocessamento é necessário identificar **pontos isolados em relação a uma camada de referência**.

Esse processo geralmente envolve inspeção manual ou múltiplas operações espaciais intermediárias, o que se torna ineficiente em datasets grandes.

Esta ferramenta automatiza o processo, permitindo identificar feições isoladas **de forma rápida, reproduzível e escalável**, especialmente em bases com dezenas de milhares de registros.

---

## 📂 Estrutura do Projeto

```
spatial-isolation-detector
├── selecao_pontos_isolados.py
├── docs
│   └── IMAGENS
│       └── interface_tool.png
└── README.md
```

---

## 📝 Licença

MIT License — livre para uso, modificação e distribuição.
