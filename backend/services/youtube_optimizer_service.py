"""
YouTube Channel Optimizer Service - Serviço Integrado Completo

Integra todos os componentes do sistema conforme documento técnico:
- DNA Semântico do Canal
- Processador de Referências (obrigatório)
- Métricas Avançadas
- Análise Preditiva completa

Este é o serviço principal que implementa TODAS as funcionalidades
descritas no documento "Simulação e Análise Preditiva para Otimização
de Conteúdo no YouTube".
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

from core.dna_semantico import ChannelSemanticDNA
from core.referencias_processor import ReferenceProcessor, Referencia
from core.metricas_avancadas import AdvancedMetricsAnalyzer, CompleteAnalysis
from models.channel import Channel
from sentence_transformers import SentenceTransformer


class YouTubeOptimizerService:
    """
    Serviço completo de otimização de conteúdo para YouTube.

    Implementa todas as funcionalidades do documento técnico:
    - Parte 1: Análise do Algoritmo
    - Parte 2: Modelagem do DNA Semântico
    - Parte 3: Fluxo Funcional
    - Parte 4: Word2Vec Obrigatório
    - Parte 5: Memória e Evolução
    - Parte 6: Saídas Avançadas
    """

    def __init__(self):
        # Modelo de embeddings semânticos
        self.sentence_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

        # Componentes principais
        self.processador_referencias: Optional[ReferenceProcessor] = None
        self.dna_canal: Optional[ChannelSemanticDNA] = None
        self.analisador_metricas: Optional[AdvancedMetricsAnalyzer] = None

        # Canal atual
        self.canal_atual: Optional[Channel] = None

        # Referências virais (para comparação)
        self.referencias_virais: List[Dict] = []

    def criar_canal(
        self,
        nome: str,
        subnicho: str,
        resumo_ideia: str,
        referencias: List[Dict]
    ) -> Dict:
        """
        PARTE 3 - Função criar_canal()

        Cria um novo canal com DNA Semântico baseado em referências obrigatórias.

        Args:
            nome: Nome do canal
            subnicho: Campo temático específico (ex: "Machine Learning para Finanças")
            resumo_ideia: Parágrafo descrevendo público-alvo, estilo e objetivos
            referencias: Lista de dicionários com:
                - 'titulo': str (OBRIGATÓRIO)
                - 'descricao': str (opcional)
                - 'transcricao': str (opcional)
                - 'tags': List[str] (opcional)

        Returns:
            Dicionário com status, canal criado e análise inicial

        Raises:
            ValueError: Se referências não forem fornecidas
        """

        # Valida inputs obrigatórios
        if not referencias or len(referencias) == 0:
            raise ValueError(
                "❌ ERRO CRÍTICO: Referências são OBRIGATÓRIAS.\n\n"
                "Para criar um canal, você DEVE fornecer referências de vídeos "
                "de sucesso no seu nicho. Isso é essencial porque:\n\n"
                "1. O sistema treina um modelo Word2Vec EXCLUSIVAMENTE com suas referências\n"
                "2. Não usamos dados externos ou pré-definidos\n"
                "3. Todo o universo semântico é inferido das referências\n\n"
                "Forneça pelo menos 3-5 títulos de vídeos virais do seu nicho."
            )

        # Converte referências para objetos Referencia
        refs_processadas = []
        for ref in referencias:
            if 'titulo' not in ref or not ref['titulo']:
                continue

            refs_processadas.append(Referencia(
                titulo=ref['titulo'],
                descricao=ref.get('descricao'),
                transcricao=ref.get('transcricao'),
                tags=ref.get('tags')
            ))

        if len(refs_processadas) < 3:
            raise ValueError(
                f"❌ Mínimo 3 referências necessárias. Você forneceu {len(refs_processadas)}."
            )

        # 1. PROCESSAMENTO DE REFERÊNCIAS
        print("🔄 Processando referências e treinando Word2Vec...")
        self.processador_referencias = ReferenceProcessor()

        resultado_processamento = self.processador_referencias.processar_referencias(
            referencias=refs_processadas,
            subnicho=subnicho,
            resumo_ideia=resumo_ideia
        )

        # 2. CRIAÇÃO DO DNA SEMÂNTICO INICIAL
        print("🧬 Criando DNA Semântico do Canal...")
        self.dna_canal = ChannelSemanticDNA()

        # Adiciona embeddings das referências ao DNA inicial
        for ref in resultado_processamento['referencias_virais']:
            # Títulos de referência definem o padrão
            self.dna_canal.adicionar_titulo(
                ref['vetor_titulo'],
                ref['titulo']
            )

            # Descrições (se disponíveis)
            if 'vetor_descricao' in ref and ref['vetor_descricao'] is not None:
                self.dna_canal.adicionar_descricao(
                    ref['vetor_descricao'],
                    ref['descricao']
                )

            # Transcrições (se disponíveis)
            if 'vetor_transcricao' in ref and ref['vetor_transcricao'] is not None:
                self.dna_canal.adicionar_video(
                    ref['vetor_transcricao'],
                    ref['titulo']  # Usa título como placeholder
                )

        # Salva referências virais para comparação futura
        self.referencias_virais = resultado_processamento['referencias_virais']

        # 3. CRIA ANALISADOR DE MÉTRICAS
        self.analisador_metricas = AdvancedMetricsAnalyzer(
            dna_canal=self.dna_canal,
            modelo_word2vec=resultado_processamento['word2vec_model']
        )

        # 4. CRIA OBJETO CHANNEL
        self.canal_atual = Channel(
            name=nome,
            niche=resultado_processamento['analise_inicial']['topicos_principais'][0]
                if resultado_processamento['analise_inicial']['topicos_principais']
                else subnicho,
            sub_niche=subnicho,
            description=resumo_ideia
        )

        # Adiciona keywords descobertas
        self.canal_atual.keywords = resultado_processamento['analise_inicial']['vocabulario_core']

        # 5. ANÁLISE DO DNA INICIAL
        estatisticas_dna = self.dna_canal.get_estatisticas_completas()

        return {
            'success': True,
            'channel_id': self.canal_atual.channel_id,
            'message': '✅ Canal criado com sucesso!',

            # Análise do processamento de referências
            'analise_referencias': {
                'total_referencias': resultado_processamento['analise_inicial']['total_referencias'],
                'corpus_size': resultado_processamento['corpus_size'],
                'vocabulario_size': resultado_processamento['vocab_size'],
                'vocabulario_core': resultado_processamento['vocabulario_nicho'][:15],
                'clusters_topicos': resultado_processamento['clusters_topicos'],
                'padroes_titulo': resultado_processamento['analise_inicial']['padroes_titulo'],
                'recomendacoes': resultado_processamento['analise_inicial']['recomendacoes_iniciais']
            },

            # Estatísticas do DNA Semântico
            'dna_semantico': {
                'magnitude': estatisticas_dna['magnitude_dna'],
                'coerencia_vetorial': estatisticas_dna['coerencia_vetorial'],
                'ruido_semantico': estatisticas_dna['ruido_semantico'],
                'forca_dna': estatisticas_dna['analise_forca'],
                'componentes': estatisticas_dna['componentes']
            },

            # Próximos passos
            'proximos_passos': [
                "1️⃣ Canal configurado e pronto para uso",
                "2️⃣ Comece analisando títulos para seus vídeos",
                "3️⃣ O DNA do canal evoluirá com cada conteúdo aprovado",
                "4️⃣ Monitore a coerência vetorial para manter identidade forte"
            ]
        }

    def analisar_titulo(
        self,
        titulo: str,
        salvar: bool = False
    ) -> Dict:
        """
        PARTE 3 - Função analisar_titulo()

        Analisa um título gerando todas as métricas avançadas da Parte 6.

        Args:
            titulo: O título a ser analisado
            salvar: Se True, adiciona ao DNA do canal após análise

        Returns:
            Análise completa com scores, justificativas e recomendações
        """

        if not self.dna_canal or not self.analisador_metricas:
            raise ValueError(
                "❌ Nenhum canal criado. Use criar_canal() primeiro."
            )

        # Gera embedding do título
        vetor_titulo = self.sentence_model.encode(titulo)

        # Análise completa usando métricas avançadas
        analise: AnaliseCompleta = self.analisador_metricas.analisar_titulo(
            titulo=titulo,
            vetor_titulo=vetor_titulo,
            titulos_virais_referencia=self.referencias_virais
        )

        # Se aprovado e salvar=True, adiciona ao DNA
        if salvar and analise.score_numerico >= 60:
            self.dna_canal.adicionar_titulo(vetor_titulo, titulo)

            # Atualiza canal
            if self.canal_atual:
                self.canal_atual.add_video({'titulo': titulo, 'status': 'titulo_aprovado'})

        # Formata resposta conforme Parte 6 do documento
        return {
            'titulo': titulo,
            'salvo': salvar and analise.score_numerico >= 60,

            # Métricas principais (0-100)
            'score_numerico': round(analise.score_numerico, 2),
            'analise_risco': round(analise.analise_risco, 2),

            # Justificativa técnica detalhada
            'justificativa_tecnica': analise.justificativa_tecnica,

            # Impacto no embedding do canal
            'impacto_no_embedding': {
                'coerencia_atual': analise.impacto_embedding['impacto_coerencia']['atual'],
                'coerencia_nova': analise.impacto_embedding['impacto_coerencia']['nova'],
                'delta_coerencia': analise.impacto_embedding['impacto_coerencia']['delta'],
                'magnitude_atual': analise.impacto_embedding['impacto_magnitude']['atual'],
                'magnitude_nova': analise.impacto_embedding['impacto_magnitude']['nova'],
                'delta_magnitude': analise.impacto_embedding['impacto_magnitude']['delta'],
                'deslocamento_graus': analise.impacto_embedding['deslocamento_vetor']['angulo_graus'],
                'efeito': analise.impacto_embedding['efeito_geral'],
                'recomendacao_impacto': analise.impacto_embedding['recomendacao']
            },

            # Probabilidades
            'probabilidade_entrega_inicial': analise.probabilidade_entrega_inicial,
            'probabilidade_escala': analise.probabilidade_escala,

            # Métricas detalhadas
            'metricas_detalhadas': {
                'similaridade_dna_canal': round(analise.similaridade_dna_canal, 3),
                'similaridade_titulos_virais': round(analise.similaridade_titulos_virais, 3),
                'densidade_semantica': round(analise.densidade_semantica, 3),
                'risco_ruptura_cluster': round(analise.risco_ruptura_cluster, 3)
            },

            # Recomendação final
            'recomendacao_final': analise.recomendacao_final,
            'proximos_passos': analise.proximos_passos
        }

    def listar_titulos(self) -> Dict:
        """
        PARTE 3 - Função listar_titulos()

        Lista todos os títulos aprovados e salvos no canal.
        """

        if not self.canal_atual:
            return {'titulos': [], 'total': 0}

        titulos_aprovados = [
            {
                'id': i,
                'titulo': video.get('titulo', ''),
                'data': video.get('added_at', '')
            }
            for i, video in enumerate(self.canal_atual.videos)
            if 'titulo' in video
        ]

        return {
            'titulos': titulos_aprovados,
            'total': len(titulos_aprovados)
        }

    def gerar_prompt_roteiro(self, id_titulo: Optional[int] = None, titulo: Optional[str] = None) -> Dict:
        """
        PARTE 3 - Função gerar_prompt_roteiro()

        Gera prompt otimizado para criação de roteiro baseado em análise vetorial.

        Args:
            id_titulo: ID do título na lista (se foi salvo)
            titulo: Texto do título (se não foi salvo)

        Returns:
            Prompt contextualizado com palavras-chave semânticas
        """

        if not self.dna_canal or not self.processador_referencias:
            raise ValueError("❌ Canal não criado")

        # Determina o título a usar
        if id_titulo is not None:
            if not self.canal_atual or id_titulo >= len(self.canal_atual.videos):
                raise ValueError(f"❌ Título com ID {id_titulo} não encontrado")
            titulo_texto = self.canal_atual.videos[id_titulo].get('titulo', '')
        elif titulo:
            titulo_texto = titulo
        else:
            raise ValueError("❌ Forneça id_titulo ou titulo")

        # Gera embedding do título
        vetor_titulo = self.sentence_model.encode(titulo_texto)

        # Extrai palavras-chave semanticamente próximas usando Word2Vec
        palavras_chave_titulo = self._extrair_palavras_chave_semanticas(
            titulo_texto,
            top_n=10
        )

        # Palavras-chave do DNA do canal
        vetor_y = self.dna_canal.calcular_vetor_y()
        palavras_chave_canal = self.canal_atual.keywords[:15]

        # Gera prompt estruturado
        prompt = self._criar_prompt_roteiro_otimizado(
            titulo=titulo_texto,
            palavras_chave_titulo=palavras_chave_titulo,
            palavras_chave_canal=palavras_chave_canal,
            subnicho=self.canal_atual.sub_niche,
            resumo=self.canal_atual.description
        )

        return {
            'success': True,
            'titulo': titulo_texto,
            'prompt_roteiro': prompt,
            'palavras_chave_titulo': palavras_chave_titulo,
            'palavras_chave_canal': palavras_chave_canal,
            'diretrizes': self._gerar_diretrizes_roteiro()
        }

    def analisar_roteiro(
        self,
        titulo: str,
        roteiro: str,
        salvar: bool = False
    ) -> Dict:
        """
        PARTE 3 - Função analisar_roteiro()

        Valida roteiro analisando coerência vetorial com título e canal.

        Args:
            titulo: Título do vídeo
            roteiro: Texto completo do roteiro
            salvar: Se True, adiciona ao DNA após aprovação

        Returns:
            Análise completa com aprovação/rejeição e feedback
        """

        if not self.dna_canal or not self.analisador_metricas:
            raise ValueError("❌ Canal não criado")

        # Gera embeddings
        vetor_titulo = self.sentence_model.encode(titulo)
        vetor_roteiro = self.sentence_model.encode(roteiro)

        # Análise completa do roteiro
        analise: AnaliseCompleta = self.analisador_metricas.analisar_roteiro(
            titulo=titulo,
            roteiro=roteiro,
            vetor_titulo=vetor_titulo,
            vetor_roteiro=vetor_roteiro
        )

        # Decisão de aprovação
        aprovado = (
            analise.score_numerico >= 60 and
            analise.similaridade_titulos_virais >= 0.4  # Coerência título-roteiro
        )

        # Se aprovado e salvar=True, adiciona ao DNA
        if aprovado and salvar:
            self.dna_canal.adicionar_video(vetor_roteiro, roteiro[:200])

            if self.canal_atual:
                self.canal_atual.add_video({
                    'titulo': titulo,
                    'roteiro': roteiro,
                    'status': 'roteiro_aprovado'
                })

        return {
            'aprovado': aprovado,
            'salvo': aprovado and salvar,
            'titulo': titulo,

            # Scores
            'score_geral': round(analise.score_numerico, 2),
            'coerencia_titulo_roteiro': round(analise.similaridade_titulos_virais, 3),
            'coerencia_canal': round(analise.similaridade_dna_canal, 3),

            # Justificativa
            'justificativa_tecnica': analise.justificativa_tecnica,

            # Impacto
            'impacto_no_embedding': analise.impacto_embedding,

            # Recomendação
            'recomendacao': analise.recomendacao_final,
            'proximos_passos': analise.proximos_passos,

            # Status
            'status': 'APROVADO ✅' if aprovado else 'PRECISA REVISAR ⚠️'
        }

    def gerar_conteudo_complementar(
        self,
        titulo: str,
        roteiro: str
    ) -> Dict:
        """
        Gera descrição, tags e prompt de thumbnail após roteiro aprovado.

        Args:
            titulo: Título do vídeo
            roteiro: Roteiro aprovado

        Returns:
            Descrição SEO, tags e prompt de thumbnail
        """

        if not self.canal_atual or not self.processador_referencias:
            raise ValueError("❌ Canal não criado")

        # Gera cada componente usando o DNA do canal
        descricao = self._gerar_descricao_seo(titulo, roteiro)
        tags = self._gerar_tags_otimizadas(titulo, roteiro)
        thumbnail_prompt = self._gerar_prompt_thumbnail(titulo)

        # Adiciona ao DNA (componentes finais)
        if descricao:
            vetor_desc = self.sentence_model.encode(descricao)
            self.dna_canal.adicionar_descricao(vetor_desc, descricao)

        if tags:
            tags_texto = ' '.join(tags)
            vetor_tags = self.sentence_model.encode(tags_texto)
            self.dna_canal.adicionar_hashtag(vetor_tags, tags_texto)

        if thumbnail_prompt:
            vetor_thumb = self.sentence_model.encode(thumbnail_prompt)
            self.dna_canal.adicionar_thumbnail(vetor_thumb, thumbnail_prompt)

        return {
            'success': True,
            'descricao': descricao,
            'tags': tags,
            'thumbnail_prompt': thumbnail_prompt
        }

    def get_estatisticas_canal(self) -> Dict:
        """
        Retorna estatísticas completas do canal e DNA Semântico.
        """

        if not self.dna_canal or not self.canal_atual:
            return {'error': 'Canal não criado'}

        stats_dna = self.dna_canal.get_estatisticas_completas()

        return {
            'canal': self.canal_atual.to_dict(),
            'dna_semantico': stats_dna,
            'referencias_virais': len(self.referencias_virais),
            'word2vec_vocab_size': len(self.processador_referencias.word2vec_model.wv)
                if self.processador_referencias and self.processador_referencias.word2vec_model
                else 0
        }

    # ============ MÉTODOS AUXILIARES ============

    def _extrair_palavras_chave_semanticas(self, texto: str, top_n: int = 10) -> List[str]:
        """Extrai palavras-chave usando Word2Vec"""
        if not self.processador_referencias or not self.processador_referencias.word2vec_model:
            return []

        import re
        tokens = re.findall(r'\b\w+\b', texto.lower())

        palavras_relacionadas = set()

        for token in tokens:
            try:
                if token in self.processador_referencias.word2vec_model.wv:
                    similares = self.processador_referencias.word2vec_model.wv.most_similar(
                        token,
                        topn=5
                    )
                    palavras_relacionadas.update([p for p, _ in similares])
            except:
                continue

        return list(palavras_relacionadas)[:top_n]

    def _criar_prompt_roteiro_otimizado(
        self,
        titulo: str,
        palavras_chave_titulo: List[str],
        palavras_chave_canal: List[str],
        subnicho: str,
        resumo: str
    ) -> str:
        """Cria prompt otimizado para geração de roteiro"""

        prompt = f"""# 🎬 Prompt para Criação de Roteiro Otimizado

## 📌 Título do Vídeo
**{titulo}**

## 🎯 Contexto do Canal
- **Nicho:** {subnicho}
- **Proposta:** {resumo}

## 🔑 Palavras-Chave Semânticas (OBRIGATÓRIO usar no roteiro)

### Do Título (incorporar naturalmente):
{', '.join(palavras_chave_titulo[:8])}

### Do Canal (manter coerência):
{', '.join(palavras_chave_canal[:12])}

## 📐 Estrutura Recomendada

### 1. GANCHO (primeiros 15 segundos)
- Apresente a promessa do título imediatamente
- Gere curiosidade ou apresente benefício claro
- Seja direto e impactante

### 2. INTRODUÇÃO (15-45 segundos)
- Contextualize brevemente o tema
- Explique o que será abordado
- Estabeleça credibilidade

### 3. DESENVOLVIMENTO (corpo principal)
- Cumpra EXATAMENTE o que o título promete
- Use as palavras-chave semânticas naturalmente
- Mantenha coerência com a identidade do canal
- Divida em seções lógicas

### 4. CONCLUSÃO (últimos 30 segundos)
- Recapitule pontos principais
- Call-to-action (inscrição, like, comentário)
- Deixe abertura para próximos vídeos

## ⚠️ REGRAS CRÍTICAS

1. **COERÊNCIA TÍTULO-ROTEIRO**: O roteiro DEVE entregar o que o título promete
2. **DENSIDADE SEMÂNTICA**: Use vocabulário alinhado com as palavras-chave fornecidas
3. **SEM CLICKBAIT**: Não prometa no título o que não será entregue no roteiro
4. **RETENÇÃO**: Estruture para manter o espectador até o final

## 🎯 Objetivo
Criar roteiro que:
- Maximize tempo de exibição (watch time)
- Mantenha coerência vetorial com o DNA do canal
- Gere engajamento orgânico
- Posicione bem nos algoritmos de recomendação

---
**Gere o roteiro completo abaixo:**
"""

        return prompt

    def _gerar_diretrizes_roteiro(self) -> List[str]:
        """Gera diretrizes para criação de roteiro"""
        return [
            "📌 Cumpra a promessa do título nos primeiros 60 segundos",
            "🎯 Use palavras-chave do canal para manter coerência vetorial",
            "⏱️ Gancho forte nos primeiros 15 segundos é crítico",
            "📊 Estruture para maximizar retenção de audiência",
            "🔄 Mantenha densidade semântica alta com vocabulário do nicho"
        ]

    def _gerar_descricao_seo(self, titulo: str, roteiro: str) -> str:
        """Gera descrição otimizada para SEO"""
        # Primeiras 2-3 frases do roteiro
        sentencas = roteiro.split('.')[:3]
        intro = '. '.join(sentencas) + '.'

        keywords = ', '.join(self.canal_atual.keywords[:10])

        descricao = f"""{intro}

🎯 Neste vídeo você vai aprender:
{self.canal_atual.sub_niche}

📌 Tópicos abordados:
- Conteúdo profundo sobre {self.canal_atual.sub_niche}
- Informações práticas e aplicáveis

🔔 Inscreva-se para mais conteúdo sobre: {keywords}

---
{self.canal_atual.description}
"""

        return descricao

    def _gerar_tags_otimizadas(self, titulo: str, roteiro: str) -> List[str]:
        """Gera tags otimizadas semanticamente"""
        import re

        # Tags do canal
        tags_canal = self.canal_atual.keywords[:10]

        # Palavras do título
        palavras_titulo = [
            w.lower() for w in re.findall(r'\b\w+\b', titulo)
            if len(w) > 3
        ]

        # Palavras-chave semânticas do roteiro
        palavras_semanticas = self._extrair_palavras_chave_semanticas(roteiro, top_n=5)

        # Combina e remove duplicatas
        todas_tags = list(set(tags_canal + palavras_titulo + palavras_semanticas + [self.canal_atual.sub_niche]))

        return todas_tags[:25]  # YouTube permite até 500 caracteres

    def _gerar_prompt_thumbnail(self, titulo: str) -> str:
        """Gera prompt para criação de thumbnail"""
        palavras_chave = self._extrair_palavras_chave_semanticas(titulo, top_n=3)

        prompt = f"""# 🎨 Prompt para Thumbnail Otimizada

## Título do Vídeo
{titulo}

## Especificações Técnicas
- Resolução: 1280x720px (16:9)
- Formato: JPG ou PNG de alta qualidade
- Tamanho: máximo 2MB

## Elementos Visuais OBRIGATÓRIOS

### 1. Texto Principal
**Extraia 3-5 palavras-chave do título:**
{' | '.join(palavras_chave[:3])}

- Fonte: Grande, bold, legível
- Contraste: Alto (texto escuro em fundo claro ou vice-versa)
- Posição: Seguindo regra dos terços

### 2. Composição
- Imagem de fundo relevante ao tema
- Espaço para tempo do vídeo (canto inferior direito)
- Expressão facial (se usar pessoa): Emocional, envolvente

### 3. Cores
- Paleta vibrante mas profissional
- Consistente com identidade do canal
- Alto contraste para chamar atenção

### 4. Estilo
- Evitar poluição visual
- Máximo 3-4 elementos principais
- Design clean e profissional

## 🎯 Objetivo
Thumbnail que:
- Maximize CTR (Click-Through Rate)
- Seja consistente com o canal
- Entregue o que promete (sem clickbait)
- Destaque-se no feed de recomendações

---
**Descrição da imagem a ser criada:**
Thumbnail com foco em {palavras_chave[0] if palavras_chave else titulo}, usando cores vibrantes e texto grande com as palavras-chave principais destacadas.
"""

        return prompt
