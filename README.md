# 🎯 YouTube Channel Vector Optimizer

Sistema **ADAPTATIVO** revolucionário de otimização de conteúdo para YouTube baseado em análise vetorial (Word2Vec) e NLP.

## 🧠 Conceito Revolucionário

Diferente de sistemas tradicionais com parâmetros fixos, este sistema **APRENDE** com seus dados:

O YouTube cria embeddings (vetores) para cada canal. Este sistema replica esse processo de forma adaptativa, criando um vetor composto **Y** para seu canal:

- **T** (Título): Vetor de títulos
- **V** (Vídeo): Vetor de transcrições/roteiros
- **D** (Descrição): Vetor de descrições
- **H** (Hashtags): Vetor de tags
- **U** (Thumbnail): Vetor de características visuais

### 🚀 Diferencial: Sistema 100% Adaptativo

❌ **NÃO** usa métricas fixas como "título deve ter 60 caracteres"
✅ **DESCOBRE** automaticamente o padrão ideal para SEU canal

O sistema:
1. Analisa a descrição do seu canal
2. Aprende com títulos de exemplo que você fornece
3. Descobre padrões automaticamente (tamanho, estrutura, estilo)
4. Usa Word2Vec para entender semanticamente seu conteúdo
5. Evolui continuamente com cada novo input

## ✨ Funcionalidades

### 1. 🎨 Gestão de Canais
- **Criar novo canal**: Define subnicho e descrição
- **Carregar canal existente**: Mantém todo histórico de aprendizado
- **Persistência completa**: Todos os vetores e padrões aprendidos são salvos

### 2. 🧪 Sistema de Aprendizado Adaptativo
- **Treina com seus dados**: Adicione títulos de exemplo do seu canal ou similares
- **Descobre padrões automaticamente**: Não precisa definir regras
- **Word2Vec customizado**: Modelo treinado especificamente para SEU conteúdo
- **Análise semântica profunda**: Entende o significado, não apenas palavras

### 3. 📊 Validação Inteligente de Títulos
- **Análise de coerência vetorial**: Compara com o padrão do canal
- **Análise de risco adaptativa**: Baseada no histórico, não em regras fixas
- **Score detalhado**: Por que funciona e quais os riscos
- **Recomendações contextuais**: Específicas para SEU canal

### 4. 📝 Geração de Conteúdo
- **Prompts contextualizados para roteiros**: Baseados no vetor do canal
- **Validação de roteiros**: Verifica coerência título ↔ roteiro ↔ canal
- **Geração automática**:
  - Descrições otimizadas para SEO
  - Tags alinhadas com o canal
  - Prompts para thumbnails

### 5. 🎯 Suporta QUALQUER Nicho
- Não há lista fixa de nichos
- Sistema descobre características de qualquer tipo de conteúdo:
  - Tecnologia, Educação, História, True Crime
  - Gaming, Lifestyle, Culinária, Negócios
  - **Qualquer nicho**: O sistema adapta-se!

## 📁 Estrutura do Projeto

```
TesteYT/
├── backend/
│   ├── core/
│   │   ├── vector_analyzer.py       # Análise vetorial adaptativa (Word2Vec)
│   │   ├── pattern_discovery.py     # Descoberta automática de padrões
│   │   └── similarity_search.py     # Busca de conteúdos similares
│   ├── models/
│   │   ├── channel.py               # Modelo de canal com vetores
│   │   └── video.py                 # Modelo de vídeo
│   ├── services/
│   │   └── channel_service.py       # Orquestrador principal
│   └── database/
│       └── storage.py               # Persistência de dados
├── frontend/
│   ├── index.html                   # Interface web
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js                   # Aplicação frontend
├── data/
│   └── channels/                    # Canais salvos (JSON)
├── requirements.txt
└── main.py                          # Servidor Flask
```

## 🚀 Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd TesteYT

# Instale as dependências
pip install -r requirements.txt

# Baixe o modelo de linguagem (português)
python -m spacy download pt_core_news_sm

# Execute a aplicação
python main.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 📖 Como Usar

### Passo 1: Criar ou Carregar Canal
1. Execute `python main.py`
2. Acesse **http://localhost:5000** no navegador
3. Escolha entre:
   - **Criar Novo Canal**: Defina nome, subnicho e descrição
   - **Carregar Canal Existente**: Continue de onde parou

### Passo 2: Treinar o Sistema (Recomendado)
- Adicione **títulos de exemplo** (seus ou de canais similares)
- O sistema aprenderá automaticamente:
  - Padrões de estrutura (tamanho, formato)
  - Vocabulário característico
  - Estilo de comunicação
- Quanto mais exemplos, mais preciso!

### Passo 3: Workflow de Criação de Conteúdo

#### 📌 1. Validar Título
1. Digite o título proposto
2. Receba análise completa:
   - Score geral de qualidade
   - Coerência com o canal
   - Análise de risco
   - Por que funciona / Por que arrisca
3. Aprove ou ajuste

#### 📝 2. Gerar Prompt de Roteiro
1. Use o título aprovado
2. Sistema gera prompt contextualizado
3. Use em IA (ChatGPT, Claude, etc.) para criar roteiro

#### ✅ 3. Validar Roteiro
1. Cole o roteiro gerado
2. Sistema valida:
   - Coerência título ↔ roteiro
   - Coerência com canal
   - Cumprimento da promessa do título

#### 🎬 4. Gerar Conteúdo Complementar
1. Com roteiro aprovado
2. Sistema gera automaticamente:
   - Descrição otimizada para SEO
   - Tags relevantes
   - Prompt para criar thumbnail

### Passo 4: Evolução Contínua
- Cada conteúdo aprovado ensina o sistema
- Padrões são refinados automaticamente
- Canal mantém coerência vetorial crescente

## 🛠️ Tecnologias

- **Python 3.8+**
- **sentence-transformers**: Embeddings semânticos multilíngues
- **gensim**: Word2Vec e análise vetorial
- **spaCy**: Processamento de linguagem natural
- **scikit-learn**: Machine learning e métricas
- **Flask**: Backend API REST
- **JavaScript/HTML/CSS**: Interface web responsiva

## 🔬 Como Funciona (Técnico)

### Análise Vetorial Adaptativa

1. **Embeddings Semânticos**:
   - Usa `paraphrase-multilingual-mpnet-base-v2` para embeddings iniciais
   - Cada texto (título, descrição, roteiro) vira um vetor de 768 dimensões

2. **Word2Vec Personalizado**:
   - Treinado com os dados específicos do seu canal
   - Aprende relações semânticas únicas do seu conteúdo
   - Atualizado continuamente com novos dados

3. **Vetor do Canal (Y)**:
   ```
   Y = 0.30×T + 0.30×V + 0.20×D + 0.15×H + 0.05×U
   ```
   - Média ponderada dos sub-vetores
   - Representa a "identidade vetorial" do canal

4. **Análise de Coerência**:
   - Similaridade de cosseno entre vetores
   - Score > 0.7: Altamente coerente
   - Score < 0.3: Desalinhado

5. **Descoberta de Padrões**:
   - Análise estatística de múltiplas dimensões
   - Identifica estruturas, vocabulário, estilos
   - Sem regras pré-definidas

## 🎯 Casos de Uso

- **Criadores de Conteúdo**: Mantenha consistência no canal
- **Agências**: Gerencie múltiplos canais com padrões únicos
- **Educadores**: Crie conteúdo didático alinhado
- **Empresas**: Conteúdo corporativo coerente

## 📈 Próximas Melhorias

- [ ] Integração com YouTube Data API v3
- [ ] Análise de thumbnails com Computer Vision
- [ ] Predição de performance (views estimadas)
- [ ] A/B testing de títulos
- [ ] Dashboard de analytics

## 📄 Licença

Este projeto é de código aberto. Use, modifique e distribua livremente.

## 🤝 Contribuições

Contribuições são bem-vindas! Abra issues e pull requests.

---

**Desenvolvido com 🧠 e análise vetorial adaptativa**
