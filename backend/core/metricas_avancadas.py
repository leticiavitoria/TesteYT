"""
Métricas Avançadas para Análise de Conteúdo

Implementa as métricas especificadas na Parte 6 do documento técnico:
- Score Numérico (0-100)
- Análise de Risco de Ruptura de Cluster
- Justificativa Técnica Matemática
- Impacto no Embedding do Canal
- Probabilidade de Entrega Inicial
- Probabilidade de Escala
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CompleteAnalysis:
    """
    Result of a complete title or script analysis.
    Implements the output structure defined in Part 6.
    """
    conteudo_analisado: str
    tipo: str  # 'titulo' ou 'roteiro'

    # Métricas principais
    score_numerico: float  # 0-100
    analise_risco: float  # 0-100

    # Análises detalhadas
    justificativa_tecnica: str
    impacto_embedding: Dict
    probabilidade_entrega_inicial: str  # 'baixa', 'média', 'alta'
    probabilidade_escala: str  # 'baixa', 'média', 'alta'

    # Métricas complementares
    similaridade_dna_canal: float
    similaridade_titulos_virais: float
    densidade_semantica: float
    risco_ruptura_cluster: float

    # Recomendações
    recomendacao_final: str
    proximos_passos: List[str]


class AdvancedMetricsAnalyzer:
    """
    Analyzer that generates advanced metrics according to technical specification.
    """

    def __init__(self, dna_canal, modelo_word2vec=None):
        """
        Args:
            dna_canal: Instance of ChannelSemanticDNA
            modelo_word2vec: Word2Vec model trained with references
        """
        self.dna_canal = dna_canal
        self.modelo_word2vec = modelo_word2vec

    def analisar_titulo(
        self,
        titulo: str,
        vetor_titulo: np.ndarray,
        titulos_virais_referencia: Optional[List[Dict]] = None
    ) -> CompleteAnalysis:
        """
        Analisa um título gerando todas as métricas avançadas.

        Args:
            titulo: Texto do título
            vetor_titulo: Embedding do título
            titulos_virais_referencia: Lista de dicionários com títulos de referência
                                      [{'texto': str, 'vetor': np.ndarray}, ...]

        Returns:
            CompleteAnalysis com todas as métricas
        """

        # 1. Similaridade com DNA do Canal
        vetor_y = self.dna_canal.calcular_vetor_y()
        if vetor_y is not None:
            sim_dna = self._cosine_similarity(vetor_titulo, vetor_y)
        else:
            sim_dna = 0.5  # Neutro se DNA ainda não existe

        # 2. Similaridade com Títulos Virais
        if titulos_virais_referencia and len(titulos_virais_referencia) > 0:
            sims_virais = [
                self._cosine_similarity(vetor_titulo, ref['vetor'])
                for ref in titulos_virais_referencia
            ]
            sim_virais = np.mean(sims_virais)
        else:
            sim_virais = 0.5  # Neutro se não há referências

        # 3. Densidade Semântica
        densidade = self._calcular_densidade_semantica(titulo, vetor_titulo)

        # 4. Risco de Ruptura de Cluster
        risco_ruptura = self._calcular_risco_ruptura_cluster(
            vetor_titulo,
            sim_dna,
            densidade
        )

        # 5. Score Numérico (0-100)
        score_numerico = self._calcular_score_numerico(
            sim_dna,
            sim_virais,
            densidade,
            risco_ruptura
        )

        # 6. Análise de Risco (0-100)
        analise_risco = risco_ruptura * 100

        # 7. Justificativa Técnica
        justificativa = self._gerar_justificativa_tecnica(
            titulo,
            sim_dna,
            sim_virais,
            densidade,
            risco_ruptura
        )

        # 8. Impacto no Embedding
        impacto = self.dna_canal.simular_adicao(vetor_titulo, 'T')

        # 9. Probabilidade de Entrega Inicial
        prob_entrega = self._calcular_probabilidade_entrega(
            score_numerico,
            analise_risco
        )

        # 10. Probabilidade de Escala
        prob_escala = self._calcular_probabilidade_escala(
            sim_virais,
            densidade,
            risco_ruptura
        )

        # 11. Recomendação Final
        recomendacao = self._gerar_recomendacao_final(
            score_numerico,
            analise_risco,
            impacto
        )

        # 12. Próximos Passos
        proximos_passos = self._gerar_proximos_passos(
            score_numerico,
            analise_risco,
            impacto
        )

        return CompleteAnalysis(
            conteudo_analisado=titulo,
            tipo='titulo',
            score_numerico=score_numerico,
            analise_risco=analise_risco,
            justificativa_tecnica=justificativa,
            impacto_embedding=impacto,
            probabilidade_entrega_inicial=prob_entrega,
            probabilidade_escala=prob_escala,
            similaridade_dna_canal=sim_dna,
            similaridade_titulos_virais=sim_virais,
            densidade_semantica=densidade,
            risco_ruptura_cluster=risco_ruptura,
            recomendacao_final=recomendacao,
            proximos_passos=proximos_passos
        )

    def analisar_roteiro(
        self,
        titulo: str,
        roteiro: str,
        vetor_titulo: np.ndarray,
        vetor_roteiro: np.ndarray
    ) -> CompleteAnalysis:
        """
        Analisa um roteiro em relação ao título e ao DNA do canal.

        Args:
            titulo: Texto do título
            roteiro: Texto do roteiro
            vetor_titulo: Embedding do título
            vetor_roteiro: Embedding do roteiro

        Returns:
            CompleteAnalysis com todas as métricas
        """

        # 1. Coerência Título-Roteiro
        coerencia_titulo_roteiro = self._cosine_similarity(vetor_titulo, vetor_roteiro)

        # 2. Similaridade com DNA do Canal
        vetor_y = self.dna_canal.calcular_vetor_y()
        if vetor_y is not None:
            sim_dna = self._cosine_similarity(vetor_roteiro, vetor_y)
        else:
            sim_dna = 0.5

        # 3. Densidade Semântica
        densidade = self._calcular_densidade_semantica(roteiro, vetor_roteiro)

        # 4. Risco de Ruptura
        risco_ruptura = self._calcular_risco_ruptura_cluster(
            vetor_roteiro,
            sim_dna,
            densidade
        )

        # 5. Score Numérico
        # Para roteiros, damos peso maior à coerência com o título
        score_numerico = (
            coerencia_titulo_roteiro * 40 +  # 40% - Cumprimento da promessa do título
            sim_dna * 35 +                     # 35% - Alinhamento com canal
            densidade * 15 +                   # 15% - Densidade semântica
            (1 - risco_ruptura) * 10          # 10% - Baixo risco
        )

        # 6. Análise de Risco
        analise_risco = risco_ruptura * 100

        # 7. Justificativa Técnica
        justificativa = self._gerar_justificativa_tecnica_roteiro(
            titulo,
            roteiro,
            coerencia_titulo_roteiro,
            sim_dna,
            densidade
        )

        # 8. Impacto no Embedding
        impacto = self.dna_canal.simular_adicao(vetor_roteiro, 'V')

        # 9. Probabilidades (baseadas na análise do roteiro)
        prob_entrega = self._calcular_probabilidade_entrega(
            score_numerico,
            analise_risco
        )

        prob_escala = 'média' if coerencia_titulo_roteiro > 0.5 else 'baixa'

        # 10. Recomendação
        recomendacao = self._gerar_recomendacao_final_roteiro(
            coerencia_titulo_roteiro,
            sim_dna,
            impacto
        )

        # 11. Próximos Passos
        proximos_passos = self._gerar_proximos_passos_roteiro(
            coerencia_titulo_roteiro,
            sim_dna,
            impacto
        )

        return CompleteAnalysis(
            conteudo_analisado=roteiro[:200] + '...',  # Trunca para exibição
            tipo='roteiro',
            score_numerico=score_numerico,
            analise_risco=analise_risco,
            justificativa_tecnica=justificativa,
            impacto_embedding=impacto,
            probabilidade_entrega_inicial=prob_entrega,
            probabilidade_escala=prob_escala,
            similaridade_dna_canal=sim_dna,
            similaridade_titulos_virais=coerencia_titulo_roteiro,  # Aqui é coerência título-roteiro
            densidade_semantica=densidade,
            risco_ruptura_cluster=risco_ruptura,
            recomendacao_final=recomendacao,
            proximos_passos=proximos_passos
        )

    def _calcular_densidade_semantica(
        self,
        texto: str,
        vetor: np.ndarray
    ) -> float:
        """
        Calcula a densidade semântica do texto.

        Densidade alta = palavras semanticamente ricas no contexto do nicho.
        Usa magnitude média dos vetores de palavras no Word2Vec.
        """
        if self.modelo_word2vec is None:
            # Fallback: usa magnitude do vetor como proxy
            return min(np.linalg.norm(vetor) / 100, 1.0)

        import re
        tokens = re.findall(r'\b\w+\b', texto.lower())

        magnitudes = []
        for token in tokens:
            try:
                if token in self.modelo_word2vec.wv:
                    vetor_palavra = self.modelo_word2vec.wv[token]
                    magnitude = np.linalg.norm(vetor_palavra)
                    magnitudes.append(magnitude)
            except:
                continue

        if not magnitudes:
            return 0.5

        densidade = np.mean(magnitudes)

        # Normaliza para 0-1
        densidade_normalizada = min(densidade / 10, 1.0)

        return float(densidade_normalizada)

    def _calcular_risco_ruptura_cluster(
        self,
        vetor: np.ndarray,
        sim_dna: float,
        densidade: float
    ) -> float:
        """
        Calcula o risco de ruptura de cluster.

        Risco alto = vetor semanticamente distante do DNA do canal
        Algoritmo do YouTube pode testá-lo em audiência errada.

        Returns:
            Score de risco (0 = sem risco, 1 = risco máximo)
        """
        # Risco inversamente proporcional à similaridade com DNA
        risco_base = 1 - sim_dna

        # Ajusta pelo densidade (baixa densidade aumenta risco)
        fator_densidade = 1 - (densidade * 0.3)

        risco_final = risco_base * fator_densidade

        return float(np.clip(risco_final, 0, 1))

    def _calcular_score_numerico(
        self,
        sim_dna: float,
        sim_virais: float,
        densidade: float,
        risco_ruptura: float
    ) -> float:
        """
        Calcula o score numérico agregado (0-100).

        Combina todas as métricas com pesos definidos no documento.
        """
        score = (
            sim_dna * 25 +           # 25% - Similaridade com DNA
            sim_virais * 20 +         # 20% - Similaridade com virais
            densidade * 15 +          # 15% - Densidade semântica
            (1 - risco_ruptura) * 25 + # 25% - Baixo risco
            0.15 * 100                # 15% - Baseline de qualidade
        )

        return float(np.clip(score, 0, 100))

    def _gerar_justificativa_tecnica(
        self,
        titulo: str,
        sim_dna: float,
        sim_virais: float,
        densidade: float,
        risco: float
    ) -> str:
        """
        Gera justificativa técnica detalhada com valores matemáticos.
        """
        analise_dna = (
            f"Similaridade de cosseno com DNA do canal: **{sim_dna:.3f}**. "
        )

        if sim_dna >= 0.7:
            analise_dna += "Título **altamente coerente** com a identidade vetorial do canal. "
        elif sim_dna >= 0.5:
            analise_dna += "Título **moderadamente coerente** com o canal. "
        elif sim_dna >= 0.3:
            analise_dna += "Título **parcialmente alinhado** com o canal. "
        else:
            analise_dna += "Título **desalinhado** com o DNA do canal. "

        analise_virais = (
            f"\n\nSimilaridade com padrões virais de referência: **{sim_virais:.3f}**. "
        )

        if sim_virais >= 0.6:
            analise_virais += "Segue **fortemente** padrões de sucesso conhecidos."
        elif sim_virais >= 0.4:
            analise_virais += "Alinhamento **adequado** com padrões de sucesso."
        else:
            analise_virais += "Padrão **inovador** (distante de referências)."

        analise_densidade = (
            f"\n\nDensidade semântica: **{densidade:.3f}**. "
        )

        if densidade >= 0.7:
            analise_densidade += "Vocabulário **semanticamente rico** no contexto do nicho."
        elif densidade >= 0.5:
            analise_densidade += "Vocabulário **adequado** para o nicho."
        else:
            analise_densidade += "Vocabulário **genérico**, pode ser mais específico."

        analise_risco = f"\n\n**Risco de ruptura de cluster: {risco:.3f}** "

        if risco < 0.3:
            analise_risco += "(BAIXO). Algoritmo do YouTube conseguirá identificar audiência-alvo facilmente."
        elif risco < 0.6:
            analise_risco += "(MÉDIO). Possível confusão inicial na entrega, mas recuperável."
        else:
            analise_risco += "(ALTO). ⚠️ Alto risco de ser testado em audiência inadequada, comprometendo alcance inicial."

        return analise_dna + analise_virais + analise_densidade + analise_risco

    def _gerar_justificativa_tecnica_roteiro(
        self,
        titulo: str,
        roteiro: str,
        coerencia_titulo: float,
        sim_dna: float,
        densidade: float
    ) -> str:
        """Gera justificativa técnica para roteiro"""

        justificativa = f"**Análise de Coerência Título-Roteiro:**\n"
        justificativa += f"Similaridade de cosseno: **{coerencia_titulo:.3f}**\n\n"

        if coerencia_titulo >= 0.6:
            justificativa += "✅ Roteiro **cumpre fortemente** a promessa do título. Alta retenção esperada.\n\n"
        elif coerencia_titulo >= 0.4:
            justificativa += "⚠️ Roteiro **parcialmente alinhado** com título. Revisar se cumpre a promessa.\n\n"
        else:
            justificativa += "❌ Roteiro **não entrega** o que o título promete. Risco de clickbait percebido.\n\n"

        justificativa += f"**Alinhamento com DNA do Canal:**\n"
        justificativa += f"Similaridade: **{sim_dna:.3f}**\n\n"

        if sim_dna >= 0.6:
            justificativa += "✅ Roteiro **reforça** a identidade do canal.\n\n"
        else:
            justificativa += "⚠️ Roteiro diverge do padrão estabelecido.\n\n"

        justificativa += f"**Densidade Semântica:** {densidade:.3f}"

        return justificativa

    def _calcular_probabilidade_entrega(
        self,
        score: float,
        risco: float
    ) -> str:
        """
        Calcula probabilidade de entrega inicial.

        YouTube testa em micro-audiências. Esta métrica indica
        a probabilidade de o algoritmo encontrar a audiência certa rapidamente.
        """
        if score >= 70 and risco < 30:
            return 'alta'
        elif score >= 50 and risco < 60:
            return 'média'
        else:
            return 'baixa'

    def _calcular_probabilidade_escala(
        self,
        sim_virais: float,
        densidade: float,
        risco: float
    ) -> str:
        """
        Calcula probabilidade de escalar além da audiência inicial.

        Conteúdo que segue padrões virais + tem densidade semântica
        + baixo risco tem maior chance de "furar a bolha".
        """
        score_escala = (
            sim_virais * 0.5 +
            densidade * 0.3 +
            (1 - risco) * 0.2
        )

        if score_escala >= 0.6:
            return 'alta'
        elif score_escala >= 0.4:
            return 'média'
        else:
            return 'baixa'

    def _gerar_recomendacao_final(
        self,
        score: float,
        risco: float,
        impacto: Dict
    ) -> str:
        """Gera recomendação final baseada nas métricas"""
        if score >= 80 and risco < 20:
            return "✅ **APROVADO EXCELENTE** - Título otimizado para máximo alcance"
        elif score >= 60 and risco < 40:
            return "✅ **APROVADO** - Título adequado, pode prosseguir"
        elif score >= 40 and risco < 60:
            return "⚠️ **REVISAR** - Título aceitável mas pode melhorar"
        else:
            return "❌ **NÃO RECOMENDADO** - Título precisa de ajustes significativos"

    def _gerar_recomendacao_final_roteiro(
        self,
        coerencia_titulo: float,
        sim_dna: float,
        impacto: Dict
    ) -> str:
        """Gera recomendação final para roteiro"""
        if coerencia_titulo >= 0.5 and sim_dna >= 0.5:
            return "✅ **ROTEIRO APROVADO** - Pronto para produção"
        elif coerencia_titulo >= 0.4 or sim_dna >= 0.4:
            return "⚠️ **REVISAR ROTEIRO** - Alguns ajustes recomendados"
        else:
            return "❌ **REFAZER ROTEIRO** - Não atende requisitos de coerência"

    def _gerar_proximos_passos(
        self,
        score: float,
        risco: float,
        impacto: Dict
    ) -> List[str]:
        """Gera lista de próximos passos recomendados"""
        passos = []

        if score >= 60:
            passos.append("1️⃣ Gerar prompt de roteiro com este título")
            passos.append("2️⃣ Criar roteiro alinhado com o título")
            passos.append("3️⃣ Validar roteiro antes da produção")
        else:
            passos.append("1️⃣ Revisar título para aumentar coerência com canal")
            passos.append("2️⃣ Usar vocabulário mais alinhado com o nicho")
            if risco > 60:
                passos.append("3️⃣ ⚠️ Reduzir distância do DNA do canal para evitar ruptura de cluster")

        if impacto['efeito_geral'] == 'diluição':
            passos.append("⚠️ Atenção: Este título pode diluir o DNA do canal")

        return passos

    def _gerar_proximos_passos_roteiro(
        self,
        coerencia_titulo: float,
        sim_dna: float,
        impacto: Dict
    ) -> List[str]:
        """Gera próximos passos para roteiro"""
        passos = []

        if coerencia_titulo >= 0.5 and sim_dna >= 0.5:
            passos.append("1️⃣ Gerar descrição otimizada")
            passos.append("2️⃣ Gerar tags relevantes")
            passos.append("3️⃣ Criar thumbnail com prompt gerado")
            passos.append("4️⃣ Produzir vídeo")
        else:
            if coerencia_titulo < 0.5:
                passos.append("1️⃣ Revisar roteiro para cumprir promessa do título")
            if sim_dna < 0.5:
                passos.append("2️⃣ Alinhar vocabulário com DNA do canal")
            passos.append("3️⃣ Re-analisar após ajustes")

        return passos

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calcula similaridade de cosseno"""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return float(dot_product / (norm_v1 * norm_v2))
