"""
YouTube Channel Optimizer - API Principal

Sistema COMPLETO de Simulação e Análise Preditiva para Otimização de Conteúdo no YouTube.

Implementa TODAS as funcionalidades descritas no documento técnico:
- DNA Semântico do Canal (Vetor Y)
- Processamento de Referências Obrigatório
- Word2Vec treinado exclusivamente com dados do usuário
- Métricas Avançadas com justificativa técnica
- Análise de Risco de Ruptura de Cluster
- Simulação de Impacto no Embedding
- Probabilidades de Entrega e Escala

Autor: Sistema baseado no documento "Simulação e Análise Preditiva para Otimização de Conteúdo no YouTube"
Data: 08 de Janeiro de 2026
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import traceback

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.youtube_optimizer_service import YouTubeOptimizerService

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Serviço principal (será criado por sessão/usuário em produção)
optimizer_service = YouTubeOptimizerService()


@app.route('/')
def index():
    """Serve a aplicação frontend"""
    return send_from_directory('frontend', 'index.html')


@app.route('/api/v2/canal/criar', methods=['POST'])
def criar_canal():
    """
    Cria um novo canal com referências OBRIGATÓRIAS.

    Body JSON esperado:
    {
        "nome": "Nome do Canal",
        "subnicho": "Machine Learning para Finanças",
        "resumo_ideia": "Canal voltado para...",
        "referencias": [
            {
                "titulo": "Como usar ML em Trading",
                "descricao": "Neste vídeo...",  # opcional
                "transcricao": "Olá pessoal...",  # opcional
                "tags": ["ml", "trading"]  # opcional
            },
            ...  (mínimo 3 referências)
        ]
    }
    """
    try:
        data = request.json

        # Valida campos obrigatórios
        campos_obrigatorios = ['nome', 'subnicho', 'resumo_ideia', 'referencias']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório ausente: {campo}'
                }), 400

        # Cria o canal
        resultado = optimizer_service.criar_canal(
            nome=data['nome'],
            subnicho=data['subnicho'],
            resumo_ideia=data['resumo_ideia'],
            referencias=data['referencias']
        )

        return jsonify(resultado)

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'tipo_erro': 'validacao'
        }), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro ao criar canal: {str(e)}',
            'tipo_erro': 'sistema'
        }), 500


@app.route('/api/v2/titulo/analisar', methods=['POST'])
def analisar_titulo():
    """
    Analisa um título gerando métricas avançadas conforme Parte 6 do documento.

    Body JSON:
    {
        "titulo": "Como Usar Machine Learning para Prever Ações",
        "salvar": false  # opcional, default=false
    }

    Retorna:
    - Score numérico (0-100)
    - Análise de risco (0-100)
    - Justificativa técnica matemática
    - Impacto no embedding do canal
    - Probabilidades de entrega e escala
    - Métricas detalhadas
    """
    try:
        data = request.json

        if 'titulo' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "titulo" é obrigatório'
            }), 400

        resultado = optimizer_service.analisar_titulo(
            titulo=data['titulo'],
            salvar=data.get('salvar', False)
        )

        return jsonify({
            'success': True,
            **resultado
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro ao analisar título: {str(e)}'
        }), 500


@app.route('/api/v2/titulos/listar', methods=['GET'])
def listar_titulos():
    """
    Lista todos os títulos aprovados e salvos no canal.
    """
    try:
        resultado = optimizer_service.listar_titulos()
        return jsonify({
            'success': True,
            **resultado
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v2/roteiro/gerar-prompt', methods=['POST'])
def gerar_prompt_roteiro():
    """
    Gera prompt otimizado para criação de roteiro.

    Body JSON:
    {
        "id_titulo": 0,  # OU
        "titulo": "Texto do título"
    }
    """
    try:
        data = request.json

        resultado = optimizer_service.gerar_prompt_roteiro(
            id_titulo=data.get('id_titulo'),
            titulo=data.get('titulo')
        )

        return jsonify(resultado)

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro ao gerar prompt: {str(e)}'
        }), 500


@app.route('/api/v2/roteiro/analisar', methods=['POST'])
def analisar_roteiro():
    """
    Analisa roteiro verificando coerência com título e canal.

    Body JSON:
    {
        "titulo": "...",
        "roteiro": "...",
        "salvar": false  # opcional
    }
    """
    try:
        data = request.json

        if 'titulo' not in data or 'roteiro' not in data:
            return jsonify({
                'success': False,
                'error': 'Campos "titulo" e "roteiro" são obrigatórios'
            }), 400

        resultado = optimizer_service.analisar_roteiro(
            titulo=data['titulo'],
            roteiro=data['roteiro'],
            salvar=data.get('salvar', False)
        )

        return jsonify({
            'success': True,
            **resultado
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro ao analisar roteiro: {str(e)}'
        }), 500


@app.route('/api/v2/conteudo/gerar-complementar', methods=['POST'])
def gerar_conteudo_complementar():
    """
    Gera descrição, tags e prompt de thumbnail após roteiro aprovado.

    Body JSON:
    {
        "titulo": "...",
        "roteiro": "..."
    }
    """
    try:
        data = request.json

        if 'titulo' not in data or 'roteiro' not in data:
            return jsonify({
                'success': False,
                'error': 'Campos "titulo" e "roteiro" são obrigatórios'
            }), 400

        resultado = optimizer_service.gerar_conteudo_complementar(
            titulo=data['titulo'],
            roteiro=data['roteiro']
        )

        return jsonify(resultado)

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro ao gerar conteúdo: {str(e)}'
        }), 500


@app.route('/api/v2/canal/estatisticas', methods=['GET'])
def get_estatisticas_canal():
    """
    Retorna estatísticas completas do canal e DNA Semântico.

    Inclui:
    - Dados do canal
    - DNA Semântico (magnitude, coerência, ruído)
    - Estatísticas de componentes
    - Análise de força do DNA
    """
    try:
        resultado = optimizer_service.get_estatisticas_canal()

        return jsonify({
            'success': True,
            **resultado
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v2/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'YouTube Channel Optimizer',
        'version': '2.0',
        'features': [
            'DNA Semântico do Canal',
            'Processamento de Referências',
            'Word2Vec Personalizado',
            'Métricas Avançadas',
            'Análise Preditiva',
            'Simulação de Impacto'
        ]
    })


@app.route('/api/v2/documentacao', methods=['GET'])
def get_documentacao():
    """Retorna documentação da API"""
    return jsonify({
        'titulo': 'YouTube Channel Optimizer API v2.0',
        'descricao': 'Sistema de Simulação e Análise Preditiva para Otimização de Conteúdo no YouTube',

        'workflow': {
            '1_criar_canal': {
                'endpoint': 'POST /api/v2/canal/criar',
                'descricao': 'Cria canal com referências OBRIGATÓRIAS',
                'obrigatorio': True,
                'campos': ['nome', 'subnicho', 'resumo_ideia', 'referencias (min 3)']
            },
            '2_analisar_titulo': {
                'endpoint': 'POST /api/v2/titulo/analisar',
                'descricao': 'Analisa título com métricas avançadas',
                'campos': ['titulo', 'salvar (opcional)']
            },
            '3_gerar_prompt_roteiro': {
                'endpoint': 'POST /api/v2/roteiro/gerar-prompt',
                'descricao': 'Gera prompt otimizado para roteiro',
                'campos': ['id_titulo OU titulo']
            },
            '4_analisar_roteiro': {
                'endpoint': 'POST /api/v2/roteiro/analisar',
                'descricao': 'Valida roteiro vs título e canal',
                'campos': ['titulo', 'roteiro', 'salvar (opcional)']
            },
            '5_gerar_complementar': {
                'endpoint': 'POST /api/v2/conteudo/gerar-complementar',
                'descricao': 'Gera descrição, tags e thumbnail',
                'campos': ['titulo', 'roteiro']
            }
        },

        'metricas_retornadas': {
            'score_numerico': 'Score agregado 0-100',
            'analise_risco': 'Risco de ruptura de cluster 0-100',
            'justificativa_tecnica': 'Explicação matemática detalhada',
            'impacto_embedding': 'Simulação de impacto no DNA',
            'probabilidade_entrega_inicial': 'Alta/Média/Baixa',
            'probabilidade_escala': 'Alta/Média/Baixa',
            'metricas_detalhadas': 'Similaridades, densidade, risco'
        },

        'fundamentos_tecnicos': {
            'dna_semantico': 'Y = w_T*T + w_V*V + w_D*D + w_H*H + w_U*U',
            'word2vec': 'Treinado exclusivamente com referências do usuário',
            'embeddings': 'Sentence-BERT multilingual (768 dimensões)',
            'coerencia': 'Similaridade de cosseno entre componentes',
            'ruido': '1 - Coerência vetorial',
            'risco_ruptura': 'Distância do vetor ao DNA do canal'
        }
    })


if __name__ == '__main__':
    print("=" * 80)
    print("🎯 YOUTUBE CHANNEL OPTIMIZER v2.0")
    print("=" * 80)
    print("\n📚 SISTEMA COMPLETO DE ANÁLISE PREDITIVA")
    print("")
    print("✅ DNA Semântico do Canal (Vetor Y)")
    print("✅ Processamento de Referências Obrigatório")
    print("✅ Word2Vec Personalizado por Nicho")
    print("✅ Métricas Avançadas com Justificativa Técnica")
    print("✅ Análise de Risco de Ruptura de Cluster")
    print("✅ Simulação de Impacto no Embedding")
    print("✅ Probabilidades de Entrega e Escala")
    print("")
    print("📡 Servidor iniciando em http://localhost:5001")
    print("📖 Documentação: http://localhost:5001/api/v2/documentacao")
    print("")
    print("=" * 80)

    # Usa porta 5001 para não conflitar com o main.py original
    app.run(debug=True, host='0.0.0.0', port=5001)
