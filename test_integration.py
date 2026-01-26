#!/usr/bin/env python3
"""
Teste de integração do sistema YouTube Channel Optimizer.
Testa o fluxo completo: criar canal → treinar → validar título
"""

import sys
sys.path.append('backend')

from services.youtube_optimizer_service import YouTubeOptimizerService

def test_integration():
    print("=" * 80)
    print("🧪 TESTE DE INTEGRAÇÃO - YouTube Channel Optimizer")
    print("=" * 80)

    # Inicializa serviço
    print("\n1️⃣ Inicializando serviço...")
    service = YouTubeOptimizerService()
    print("✅ Serviço inicializado")

    # Cria canal sem referências (modo frontend)
    print("\n2️⃣ Criando canal SEM referências...")
    resultado_canal = service.criar_canal(
        nome="Canal de IA",
        subnicho="Inteligência Artificial",
        resumo_ideia="Canal sobre IA e Machine Learning",
        referencias=[]
    )
    print(f"✅ Canal criado: {resultado_canal['channel_id']}")
    print(f"   Status: {resultado_canal['status']}")

    # Treina com títulos de exemplo
    print("\n3️⃣ Treinando sistema com títulos de exemplo...")
    titulos_exemplo = [
        "Como usar Machine Learning para prever ações",
        "Deep Learning explicado de forma simples",
        "Redes Neurais: Guia completo para iniciantes",
        "Python para Data Science: Tutorial completo",
        "Inteligência Artificial no mercado financeiro"
    ]

    resultado_treino = service.treinar_canal(titulos=titulos_exemplo)
    print(f"✅ Sistema treinado com {resultado_treino['titles_learned']} títulos")
    print(f"   Vocabulário descoberto: {len(resultado_treino['analise_treinamento']['vocabulario_core'])} palavras-chave")

    # Valida um título
    print("\n4️⃣ Validando título...")
    titulo_teste = "Como criar uma rede neural do zero com Python"

    resultado_analise = service.analisar_titulo(
        titulo=titulo_teste,
        salvar=False
    )

    print(f"✅ Título analisado: '{titulo_teste}'")
    print(f"   Score: {resultado_analise['score_numerico']}/100")
    print(f"   Risco: {resultado_analise['analise_risco']}/100")
    print(f"   Recomendação: {resultado_analise['recomendacao_final']}")

    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 80)

    # Retorna True se o score for razoável
    return resultado_analise['score_numerico'] > 0

if __name__ == '__main__':
    try:
        success = test_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
