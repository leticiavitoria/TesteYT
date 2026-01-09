# 🔗 Integração Frontend-Backend - YouTube Channel Optimizer

## ✅ STATUS: TOTALMENTE INTEGRADO

Todos os códigos foram ajustados para que as variáveis do **frontend** e **backend** estejam **perfeitamente alinhadas**.

---

## 📋 Fluxo Completo da Aplicação

### 1️⃣ **Criar Canal** (`/api/channel/create`)

**Frontend envia:**
```json
{
  "name": "Nome do Canal",
  "sub_niche": "Machine Learning",
  "description": "Descrição do canal..."
}
```

**Backend recebe e processa:**
- Converte `name` → `nome`
- Converte `sub_niche` → `subnicho`
- Converte `description` → `resumo_ideia`
- Cria canal SEM referências (modo não treinado)
- Retorna `channel_id` e `status: 'nao_treinado'`

**Resposta:**
```json
{
  "success": true,
  "channel_id": "uuid-123",
  "message": "✅ Canal criado com sucesso!",
  "status": "nao_treinado",
  "proximos_passos": [...]
}
```

---

### 2️⃣ **Treinar Sistema** (`/api/channel/train`)

**Frontend envia:**
```json
{
  "channel_id": "uuid-123",
  "titles": [
    "Como usar IA para investir",
    "Machine Learning no mercado financeiro",
    "Análise preditiva com Python"
  ]
}
```

**Backend processa:**
- Valida mínimo 3 títulos
- Converte `titles` para referências
- Treina Word2Vec exclusivamente com esses títulos
- Cria DNA Semântico inicial
- Inicializa analisador de métricas

**Resposta:**
```json
{
  "success": true,
  "titles_learned": 3,
  "message": "✅ Sistema treinado com sucesso!",
  "analise_treinamento": {
    "corpus_size": 150,
    "vocabulario_size": 45,
    "vocabulario_core": ["machine", "learning", "trading", ...],
    "padroes_descobertos": {...}
  }
}
```

---

### 3️⃣ **Validar Título** (`/api/title/validate`)

**Frontend envia:**
```json
{
  "channel_id": "uuid-123",
  "title": "Como usar Deep Learning para prever Bitcoin"
}
```

**Backend processa:**
- Verifica se canal está treinado
- Gera embedding do título
- Calcula métricas avançadas:
  - Similaridade com DNA do canal
  - Similaridade com títulos virais
  - Densidade semântica
  - Risco de ruptura de cluster
- Gera justificativa técnica

**Resposta:**
```json
{
  "success": true,
  "title": "Como usar Deep Learning para prever Bitcoin",
  "overall_score": 87.5,
  "approved": true,
  "final_recommendation": "✅ Título aprovado",
  "why_it_works": [
    "Alta coerência com DNA do canal (82%)",
    "Alinhado com padrões de títulos de sucesso (78%)",
    "Baixo risco de confundir o algoritmo"
  ],
  "why_risk": [
    "Nenhum risco crítico identificado"
  ],
  "vector_analysis": {
    "coherence_with_channel": { "score": 0.82 },
    "semantic_analysis": { "channel_alignment": 0.82 },
    "risk_assessment": { "risk_level": "baixo" }
  }
}
```

---

### 4️⃣ **Gerar Prompt de Roteiro** (`/api/script/generate-prompt`)

**Frontend envia:**
```json
{
  "channel_id": "uuid-123",
  "title": "Como usar Deep Learning para prever Bitcoin"
}
```

**Backend retorna:**
```json
{
  "success": true,
  "script_prompt": "Prompt otimizado para gerar roteiro...",
  "guidelines": [
    "Mantenha coerência com DNA do canal",
    "Use vocabulário do nicho",
    ...
  ]
}
```

---

### 5️⃣ **Validar Roteiro** (`/api/script/validate`)

**Frontend envia:**
```json
{
  "channel_id": "uuid-123",
  "title": "Como usar Deep Learning para prever Bitcoin",
  "script": "Olá! Hoje vamos explorar..."
}
```

**Backend retorna:**
```json
{
  "success": true,
  "approved": true,
  "recommendation": "✅ Roteiro aprovado",
  "coherence_with_title": {
    "score": 0.89,
    "message": "Excelente coerência"
  },
  "coherence_with_channel": {
    "score": 0.85,
    "message": "Alinhado com DNA"
  },
  "feedback": [...]
}
```

---

### 6️⃣ **Gerar Conteúdo Complementar** (`/api/content/generate`)

**Frontend envia:**
```json
{
  "channel_id": "uuid-123",
  "title": "Como usar Deep Learning para prever Bitcoin",
  "script": "Olá! Hoje vamos explorar..."
}
```

**Backend retorna:**
```json
{
  "success": true,
  "description": "Descrição otimizada do vídeo...",
  "tags": ["deep learning", "bitcoin", "crypto", ...],
  "thumbnail_prompt": "Prompt para gerar thumbnail..."
}
```

---

## 🔄 Mapeamento de Variáveis

### Frontend → Backend

| Frontend        | Backend         | Endpoint                    |
|----------------|-----------------|----------------------------|
| `name`         | `nome`          | `/api/channel/create`      |
| `sub_niche`    | `subnicho`      | `/api/channel/create`      |
| `description`  | `resumo_ideia`  | `/api/channel/create`      |
| `titles`       | `titulos`       | `/api/channel/train`       |
| `title`        | `titulo`        | `/api/title/validate`      |
| `script`       | `roteiro`       | `/api/script/validate`     |

### Backend → Frontend

| Backend                      | Frontend                        |
|-----------------------------|---------------------------------|
| `score_numerico`            | `overall_score`                 |
| `pontos_fortes`             | `why_it_works`                  |
| `pontos_fracos`             | `why_risk`                      |
| `recomendacao_final`        | `final_recommendation`          |
| `similaridade_dna_canal`    | `vector_analysis.coherence...`  |

---

## 🎯 Classes Traduzidas para Inglês

Todas as classes agora estão em **inglês**:

| Português (antigo)              | Inglês (atual)              |
|--------------------------------|----------------------------|
| `ProcessadorTexto`             | `TextProcessor`            |
| `ProcessadorReferencias`       | `ReferenceProcessor`       |
| `ComponenteVetorial`           | `VectorComponent`          |
| `DNASemanticoCanal`            | `ChannelSemanticDNA`       |
| `AnalisadorMetricasAvancadas`  | `AdvancedMetricsAnalyzer`  |
| `AnaliseCompleta`              | `CompleteAnalysis`         |

---

## ✅ Sistema Funcionando

**Servidor Flask:** `http://localhost:5000`

**Endpoints disponíveis:**
- `GET /` - Frontend
- `GET /api/health` - Health check
- `POST /api/channel/create` - Criar canal
- `POST /api/channel/train` - Treinar sistema
- `POST /api/title/validate` - Validar título
- `POST /api/script/generate-prompt` - Gerar prompt
- `POST /api/script/validate` - Validar roteiro
- `POST /api/content/generate` - Gerar conteúdo

**Para iniciar:**
```bash
python3 main_optimizer.py
```

---

## 🔧 Principais Correções Realizadas

1. ✅ Backend aceita canal sem referências inicialmente
2. ✅ Método `treinar_canal()` implementado
3. ✅ Todas as variáveis alinhadas (frontend ↔ backend)
4. ✅ Classes traduzidas para inglês
5. ✅ Respostas formatadas para frontend
6. ✅ Validação de canal treinado antes de análises
7. ✅ Campos `why_it_works` e `why_risk` adicionados

---

## 📦 Dependências Instaladas

- ✅ Flask 3.1.2
- ✅ flask-cors 6.0.2
- ✅ gensim 4.3.2
- ✅ sentence-transformers 5.2.0
- ✅ scikit-learn (scipy 1.16.3)
- ✅ numpy 2.4.0

**Tudo está pronto para uso!** 🚀
