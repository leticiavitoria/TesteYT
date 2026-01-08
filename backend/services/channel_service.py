"""
Serviço principal de gerenciamento de canais.
Orquestra todos os componentes adaptativos.
"""

from typing import Dict, List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.channel import Channel
from models.video import Video
from core.vector_analyzer import AdaptiveVectorAnalyzer
from core.pattern_discovery import PatternDiscoveryEngine
from core.similarity_search import SimilaritySearchEngine


class ChannelService:
    """
    Serviço principal que coordena todo o sistema de análise e geração de conteúdo.
    """

    def __init__(self):
        self.vector_analyzer = AdaptiveVectorAnalyzer()
        self.pattern_engine = PatternDiscoveryEngine()
        self.similarity_engine = SimilaritySearchEngine()

        self.current_channel: Optional[Channel] = None

    def create_new_channel(
        self,
        name: str,
        sub_niche: str,
        description: str
    ) -> Dict:
        """
        Cria um novo canal e inicializa o sistema de aprendizado.
        """
        # Cria o canal
        self.current_channel = Channel(
            name=name,
            niche="",  # Será descoberto automaticamente
            sub_niche=sub_niche,
            description=description
        )

        # Adiciona descrição ao vetor analyzer para começar aprendizado
        self.vector_analyzer.add_training_data(description, 'descriptions')

        # Descobre características iniciais
        initial_analysis = self._discover_initial_characteristics(description, sub_niche)

        return {
            'success': True,
            'channel_id': self.current_channel.channel_id,
            'message': 'Canal criado com sucesso!',
            'initial_analysis': initial_analysis
        }

    def _discover_initial_characteristics(self, description: str, sub_niche: str) -> Dict:
        """
        Descobre características iniciais do canal baseado na descrição.
        """
        # Analisa a descrição para entender o canal
        desc_vector = self.vector_analyzer.sentence_model.encode(description)

        # Extrai palavras-chave da descrição
        from sentence_transformers import util

        # Sugere palavras-chave iniciais baseadas na descrição
        suggested_keywords = self._extract_initial_keywords(description, sub_niche)

        return {
            'suggested_keywords': suggested_keywords,
            'niche_detected': sub_niche,
            'learning_status': 'initialized',
            'next_steps': [
                '1. Adicione títulos de exemplo do seu canal ou de canais similares',
                '2. O sistema aprenderá os padrões automaticamente',
                '3. Quanto mais exemplos, mais preciso o sistema fica'
            ]
        }

    def _extract_initial_keywords(self, description: str, sub_niche: str) -> List[str]:
        """Extrai palavras-chave iniciais"""
        import re
        from collections import Counter

        # Limpa e tokeniza
        words = re.findall(r'\b\w+\b', description.lower())
        words = [w for w in words if len(w) > 3]  # Remove palavras muito curtas

        # Remove stopwords básicas
        stopwords = {
            'sobre', 'para', 'com', 'como', 'mais', 'muito', 'também',
            'esse', 'esse', 'essa', 'seus', 'suas', 'nosso', 'nossa'
        }
        words = [w for w in words if w not in stopwords]

        # Adiciona sub-nicho
        keywords = [sub_niche] + list(set(words))[:10]

        return keywords[:15]

    def add_example_titles(self, titles: List[str]) -> Dict:
        """
        Adiciona títulos de exemplo para o sistema aprender.
        Pode ser do próprio canal ou de canais similares de sucesso.
        """
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        # Adiciona cada título ao sistema de aprendizado
        for title in titles:
            self.vector_analyzer.add_training_data(title, 'titles')

        # Descobre padrões nos títulos
        patterns = self.pattern_engine.analyze_content_batch(titles)

        # Analisa títulos de sucesso
        success_analysis = self.similarity_engine.analyze_successful_titles(titles)

        # Atualiza keywords do canal
        self.current_channel.keywords = self._update_keywords_from_patterns(patterns)

        return {
            'success': True,
            'titles_learned': len(titles),
            'patterns_discovered': patterns,
            'success_analysis': success_analysis,
            'learned_guidelines': self.pattern_engine.get_learned_guidelines(),
            'message': f'Sistema aprendeu com {len(titles)} títulos!'
        }

    def _update_keywords_from_patterns(self, patterns: Dict) -> List[str]:
        """Atualiza keywords baseado nos padrões descobertos"""
        if 'vocabulary' in patterns and 'top_words' in patterns['vocabulary']:
            return [word for word, _ in patterns['vocabulary']['top_words'][:30]]
        return self.current_channel.keywords

    def validate_title(self, title: str) -> Dict:
        """
        Valida um título usando análise vetorial adaptativa.
        Retorna análise completa com risco, coerência e recomendações.
        """
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        # Análise vetorial
        vector_analysis = self.vector_analyzer.analyze_title(
            title,
            self.current_channel.to_dict()
        )

        # Análise de padrões
        pattern_evaluation = self.pattern_engine.evaluate_content_against_patterns(title)

        # Análise de performance potencial
        learned_patterns = self.similarity_engine.analyzed_content
        if learned_patterns:
            performance_potential = self.similarity_engine.evaluate_title_performance_potential(
                title,
                {
                    'structure': pattern_evaluation,
                    'keywords': {'top_words': [(k, 1) for k in self.current_channel.keywords]},
                    'strategies': []
                }
            )
        else:
            performance_potential = {'score': 50, 'rating': 'Em aprendizado'}

        # Combina todas as análises
        combined_score = self._calculate_combined_score(
            vector_analysis,
            pattern_evaluation,
            performance_potential
        )

        return {
            'title': title,
            'approved': combined_score > 60,
            'overall_score': combined_score,
            'vector_analysis': vector_analysis,
            'pattern_analysis': pattern_evaluation,
            'performance_potential': performance_potential,
            'final_recommendation': self._generate_final_recommendation(combined_score),
            'why_it_works': self._explain_why_it_works(vector_analysis, pattern_evaluation),
            'why_risk': self._explain_risks(vector_analysis, pattern_evaluation)
        }

    def _calculate_combined_score(
        self,
        vector_analysis: Dict,
        pattern_evaluation: Dict,
        performance_potential: Dict
    ) -> float:
        """Calcula score combinado de todas as análises"""
        # Score vetorial (0-100)
        coherence_score = vector_analysis['coherence_with_channel']['score'] * 100
        semantic_score = vector_analysis['semantic_analysis']['channel_alignment'] * 100
        risk_score = (1 - vector_analysis['risk_assessment']['risk_score']) * 100

        # Score de padrões (0-100)
        pattern_score = pattern_evaluation.get('score', 0.5) * 100

        # Score de performance (0-100)
        perf_score = performance_potential.get('score', 50)

        # Média ponderada
        combined = (
            coherence_score * 0.25 +
            semantic_score * 0.20 +
            risk_score * 0.25 +
            pattern_score * 0.15 +
            perf_score * 0.15
        )

        return min(combined, 100)

    def _generate_final_recommendation(self, score: float) -> str:
        """Gera recomendação final baseada no score"""
        if score >= 80:
            return "✅ APROVADO - Título excelente! Altamente alinhado com o canal."
        elif score >= 60:
            return "✅ APROVADO - Título bom, pode prosseguir."
        elif score >= 40:
            return "⚠️ REVISAR - Título aceitável, mas pode melhorar."
        else:
            return "❌ REPROVAR - Título precisa de ajustes significativos."

    def _explain_why_it_works(self, vector_analysis: Dict, pattern_analysis: Dict) -> List[str]:
        """Explica por que o título funciona"""
        reasons = []

        if vector_analysis['coherence_with_channel']['is_coherent']:
            reasons.append(
                f"✅ Coerente com o padrão do canal ({vector_analysis['coherence_with_channel']['score']:.1%})"
            )

        if vector_analysis['semantic_analysis']['is_aligned']:
            reasons.append(
                f"✅ Alinhamento semântico forte com a descrição do canal"
            )

        if pattern_analysis.get('matches'):
            reasons.extend(pattern_analysis['matches'])

        return reasons or ["Sistema em fase de aprendizado"]

    def _explain_risks(self, vector_analysis: Dict, pattern_analysis: Dict) -> List[str]:
        """Explica os riscos do título"""
        risks = []

        risk_level = vector_analysis['risk_assessment']['risk_level']
        if risk_level == 'alto':
            risks.append(
                "⚠️ RISCO ALTO: Título muito diferente do padrão estabelecido - pode confundir o algoritmo do YouTube"
            )
        elif risk_level == 'médio':
            risks.append(
                "⚠️ RISCO MÉDIO: Título parcialmente diferente - teste com cautela"
            )

        if not vector_analysis['semantic_analysis']['is_aligned']:
            risks.append(
                "⚠️ Baixo alinhamento semântico - pode atrair público errado"
            )

        if pattern_analysis.get('mismatches'):
            risks.extend(pattern_analysis['mismatches'])

        return risks or ["✅ Sem riscos identificados"]

    def generate_script_prompt(self, approved_title: str) -> Dict:
        """
        Gera prompt para criar roteiro baseado no título aprovado.
        """
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        # Analisa o título para entender o contexto
        title_analysis = self.vector_analyzer.analyze_title(
            approved_title,
            self.current_channel.to_dict()
        )

        # Gera prompt contextualizado
        prompt = self._create_script_prompt(
            approved_title,
            self.current_channel,
            title_analysis
        )

        return {
            'success': True,
            'title': approved_title,
            'script_prompt': prompt,
            'guidelines': self._get_script_guidelines()
        }

    def _create_script_prompt(
        self,
        title: str,
        channel: Channel,
        title_analysis: Dict
    ) -> str:
        """Cria prompt para geração de roteiro"""
        prompt = f"""# Prompt para Roteiro de Vídeo

## Título do Vídeo
{title}

## Contexto do Canal
- Nome: {channel.name}
- Nicho: {channel.sub_niche}
- Descrição: {channel.description}
- Palavras-chave principais: {', '.join(channel.keywords[:10])}

## Diretrizes de Conteúdo
Baseado na análise do canal, o roteiro deve:

1. **Tom e Estilo**
   - Manter coerência com o vetor do canal (similaridade atual: {title_analysis['coherence_with_channel']['score']:.1%})
   - Seguir a identidade estabelecida do canal

2. **Estrutura do Roteiro**
   - Gancho inicial forte (primeiros 15 segundos)
   - Desenvolvimento coerente com o título
   - Call-to-action no final

3. **Vocabulário**
   - Usar vocabulário alinhado com: {', '.join(channel.keywords[:5])}
   - Manter consistência semântica

4. **Duração Sugerida**
   - Avaliar complexidade do tema e ajustar duração

## Instruções
Crie um roteiro completo que:
- Entregue o que o título promete
- Mantenha coerência vetorial com o canal
- Use linguagem natural e envolvente
- Inclua momentos de retenção de audiência

---
Gere o roteiro abaixo:
"""
        return prompt

    def _get_script_guidelines(self) -> List[str]:
        """Retorna diretrizes para criação de roteiro"""
        guidelines = self.pattern_engine.get_learned_guidelines()

        if guidelines.get('status') == 'learning':
            return [
                "Sistema em aprendizado - adicione mais exemplos",
                "Mantenha coerência com a descrição do canal",
                "Use vocabulário natural e envolvente"
            ]

        return [
            f"Mantenha coerência com o padrão do canal",
            "Entregue o que o título promete",
            "Use linguagem clara e direta",
            "Inclua gancho forte no início"
        ]

    def validate_script(self, title: str, script: str) -> Dict:
        """
        Valida o roteiro analisando coerência vetorial com o título e canal.
        """
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        # Adiciona script ao aprendizado
        self.vector_analyzer.add_training_data(script, 'scripts')

        # Análise vetorial do script
        script_vector = self.vector_analyzer.sentence_model.encode(script)
        title_vector = self.vector_analyzer.sentence_model.encode(title)

        # Coerência título-roteiro
        title_script_coherence = self.vector_analyzer._cosine_similarity(
            title_vector,
            script_vector
        )

        # Coerência com o canal
        channel_coherence = self.vector_analyzer._calculate_channel_coherence(
            script_vector,
            'scripts'
        )

        # Análise de padrões
        pattern_eval = self.pattern_engine.evaluate_content_against_patterns(script)

        # Decisão
        is_approved = (
            title_script_coherence > 0.4 and
            channel_coherence['is_coherent'] and
            pattern_eval.get('score', 0) > 0.5
        )

        return {
            'approved': is_approved,
            'title': title,
            'coherence_with_title': {
                'score': float(title_script_coherence),
                'is_coherent': title_script_coherence > 0.4,
                'message': 'Roteiro alinhado com título' if title_script_coherence > 0.4 else 'Roteiro desalinhado com título'
            },
            'coherence_with_channel': channel_coherence,
            'pattern_analysis': pattern_eval,
            'recommendation': 'APROVADO ✅' if is_approved else 'PRECISA REVISAR ⚠️',
            'feedback': self._generate_script_feedback(
                title_script_coherence,
                channel_coherence,
                pattern_eval
            )
        }

    def _generate_script_feedback(
        self,
        title_coherence: float,
        channel_coherence: Dict,
        pattern_eval: Dict
    ) -> List[str]:
        """Gera feedback sobre o roteiro"""
        feedback = []

        if title_coherence < 0.4:
            feedback.append("⚠️ Roteiro não entrega o que o título promete")
        else:
            feedback.append("✅ Roteiro coerente com o título")

        if not channel_coherence['is_coherent']:
            feedback.append("⚠️ Roteiro destoa do padrão do canal")
        else:
            feedback.append("✅ Roteiro alinhado com o canal")

        if pattern_eval.get('score', 0) < 0.5:
            feedback.append("⚠️ Estrutura do roteiro diferente do padrão")

        if pattern_eval.get('recommendations'):
            feedback.extend(pattern_eval['recommendations'])

        return feedback

    def generate_complementary_content(self, title: str, script: str) -> Dict:
        """
        Gera descrição, tags e prompt de thumbnail após roteiro aprovado.
        """
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        # Gera cada componente
        description = self._generate_description(title, script)
        tags = self._generate_tags(title, script)
        thumbnail_prompt = self._generate_thumbnail_prompt(title)

        return {
            'success': True,
            'description': description,
            'tags': tags,
            'thumbnail_prompt': thumbnail_prompt
        }

    def _generate_description(self, title: str, script: str) -> str:
        """Gera descrição otimizada para SEO"""
        # Extrai primeiras frases do roteiro
        sentences = script.split('.')[:3]
        intro = '. '.join(sentences) + '.'

        keywords_text = ', '.join(self.current_channel.keywords[:10])

        description = f"""{intro}

🎯 Neste vídeo você vai aprender sobre: {', '.join(self.current_channel.keywords[:5])}

📌 Tópicos abordados:
- Conteúdo relevante baseado no roteiro
- Informações valiosas sobre {self.current_channel.sub_niche}

🔔 Se inscreva no canal para mais conteúdo sobre {self.current_channel.sub_niche}!

#️⃣ Tags: {keywords_text}

---
{self.current_channel.description}
"""
        return description

    def _generate_tags(self, title: str, script: str) -> List[str]:
        """Gera tags otimizadas"""
        import re
        from collections import Counter

        # Tags do canal
        channel_tags = self.current_channel.keywords[:15]

        # Extrai palavras do título
        title_words = [w.lower() for w in re.findall(r'\b\w+\b', title) if len(w) > 3]

        # Combina e remove duplicatas
        all_tags = list(set(channel_tags + title_words + [self.current_channel.sub_niche]))

        return all_tags[:20]

    def _generate_thumbnail_prompt(self, title: str) -> str:
        """Gera prompt para criação de thumbnail"""
        prompt = f"""# Prompt para Thumbnail

## Título do Vídeo
{title}

## Especificações
- Resolução: 1280x720px (16:9)
- Formato: JPG ou PNG
- Tamanho máximo: 2MB

## Elementos Visuais
1. **Texto Principal**: Versão curta e impactante do título
   - Sugestão: Extrair 3-5 palavras-chave principais
   - Fonte grande e legível
   - Alto contraste com fundo

2. **Cores**
   - Usar cores vibrantes e contrastantes
   - Evitar muito texto

3. **Composição**
   - Regra dos terços
   - Foco no elemento principal
   - Deixar espaço para o tempo do vídeo (canto inferior)

## Estilo
- Consistente com identidade do canal
- Atrativo mas não enganoso
- Profissional

## Palavras-chave para a imagem
{', '.join(self.current_channel.keywords[:5])}
"""
        return prompt

    def save_video_to_channel(self, video_data: Dict) -> Dict:
        """Salva vídeo completo no histórico do canal"""
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        self.current_channel.add_video(video_data)

        # Aprende com o sucesso
        if video_data.get('title'):
            self.vector_analyzer.learn_from_feedback(
                video_data['title'],
                'titles',
                True
            )

        return {
            'success': True,
            'message': 'Vídeo adicionado ao canal!',
            'total_videos': len(self.current_channel.videos)
        }

    def get_channel_summary(self) -> Dict:
        """Retorna resumo completo do canal e aprendizado"""
        if not self.current_channel:
            return {'error': 'Nenhum canal criado'}

        learned_guidelines = self.pattern_engine.get_learned_guidelines()

        return {
            'channel': self.current_channel.to_dict(),
            'learned_guidelines': learned_guidelines,
            'learning_progress': {
                'titles_learned': len(self.vector_analyzer.channel_vectors['titles']),
                'scripts_analyzed': len(self.vector_analyzer.channel_vectors['scripts']),
                'descriptions_analyzed': len(self.vector_analyzer.channel_vectors['descriptions']),
                'total_training_data': len(self.vector_analyzer.training_corpus)
            },
            'channel_embedding_ready': self.vector_analyzer.get_channel_embedding() is not None
        }
