# Criando resumos de estudos com IA

## Overview
Gastando tempo pra ganhar tempo com [GPT](https://platform.openai.com) e [crewAI](https://crewai.com).

## Requisitos
- Python 3.10 or higher
- An [OpenAI](https://platform.openai.com) API key
- (logo subirei o requirements.txt)

## Uso e Testes

### Extrair Transcrição de Videos do Youtube
```python
python TranscriptVideoExtractor.py
```

Cógido simples que solicita a URL do vídeo que deseja extrair a transcrição, lembrando que para que possa ser resumido com `main.py` é necessário nomear o arquivo sempre com `.pdf` , criando o arquivo na pasta `documents/`.


### Gerando Resumos 
```python
python main.py
```
O programa irá procurar e listar os arquivos `.pdf` localizados na pasta `documents\`, permitindo digitar um valor correspondente ao arquivo desejado.
Também será necessário definir o `context_topic`, para garantir que os prompts definidos nos agentes e tarefas extraim apenas as informações desejadas.
Por fim será solicitado o nome da pasta que sera criada para receber os outputs específicos daquela execução.

### Meus Agentes e Tarefas.


#### Agentes

`topic_researcher` : _Especializado em extrair informações relevantes de aulas, palestras e artigos._

`academic_reviewer` : _Especializado em revisar e identificar métodos específicos apresentados em contextos acadêmicos._

`ref_specialist` : _Especializado em identificar e descrever websites e referências mencionadas._

`prof` : _Escrever um tutorial (guia) passo a passo detalhado para o projeto apresentado na aula'_

`research_writer` : _Capaz de realizar pesquisas detalhadas e escrever documentos estruturados sobre métodos acadêmicos_

#### Tarefas

`list_topics_task` : _Listar todos os tópicos abordados_

`academic_review_task` : _Identificar as técnicas e métodos apresentados_

`website_list_task` : _Listar sites mencionados e outras referências_

`tutorial_write_task` : _Produzir um guia/aula_

`research_write_task` : _Com base nos materiais fornecidos pelos outros agentes, escrever um relatório estruturado de todo conteúdo_

```
"\n- **Tópicos:** a lista dos tópicos definidos"
"\n- **Objetivos:** Descreva os objetivos do estudo."
"\n- **Lacuna de pesquisa:** Identifique a lacuna de pesquisa que o estudo pretende preencher."
"\n- **Metodologia:** Detalhe os métodos utilizados no estudo."
"\n- **Conjunto de dados:** Descreva o conjunto de dados usado no estudo."
"\n- **Resultados:** Resuma as principais descobertas do estudo."
"\n- **Limitações:** Discuta as limitações do estudo."
"\n- **Conclusão:** Forneça a conclusão do estudo."
"\n- **Direções Futuras:** Sugira possíveis direções para pesquisas futuras."
"\n- **Avaliações:** Inclua quaisquer avaliações ou estimativas feitas no estudo."
```

## Exemplos

### Artigos

#### [Entropy–Based Diversification Approach for Bio–Computing Methods](https://www.mdpi.com/1099-4300/24/9/1293)
- **Resumo:** [Link para o Resumo](https://github.com/NonakaVal/lazy_review/blob/main/art-biocomputing/final_document.md)
- **Arquivos `md`:** [Ver Arquivos](https://github.com/NonakaVal/lazy_review/tree/main/art-biocomputing)
- **Descrição:** Este artigo explora uma abordagem de diversificação baseada em entropia para métodos de bioinformática.

#### [Machine Learning Algorithms for Diabetes Prediction](https://www.sciencedirect.com/science/article/pii/S1877050920300557)
- **Resumo:** [Link para o Resumo](https://github.com/NonakaVal/lazy_review/blob/main/art-Diabetes-Prediction-using-ML-Algorithms/final_document.md)
- **Arquivos `md`:** [Ver Arquivos](https://github.com/NonakaVal/lazy_review/tree/main/art-Diabetes-Prediction-using-ML-Algorithms)
- **Descrição:** Este artigo discute diferentes algoritmos de aprendizado de máquina para previsão de diabetes.

### Vídeos

#### [Machine Learning: Tutorial prático usando apenas o navegador](https://www.youtube.com/watch?v=JyGGMyR3x5I)
- **Resumo:** [Link para o Resumo](https://github.com/NonakaVal/lazy_review/blob/main/vid-dechamps/documento_final.md)
- **Arquivos `md`:** [Ver Arquivos](https://github.com/NonakaVal/lazy_review/tree/main/vid-dechamps)
- **Descrição:** Tutorial prático que ensina conceitos de machine learning usando apenas um navegador web.

#### [Um resumo sobre aprender com anotações](https://www.youtube.com/watch?v=cQ22PERTCBI&t=3s)
- **Resumo:** [Link para o Resumo](https://github.com/NonakaVal/lazy_review/blob/main/vid-meu-video/documento_final.md)
- **Arquivos `md`:** [Ver Arquivos](https://github.com/NonakaVal/lazy_review/tree/main/vid-meu-video)
- **Descrição:** Vídeo que explora técnicas eficazes para aprender com anotações durante o estudo.

---

Para explorar mais artigos e vídeos, visite [Meu Repositório de Revisões](https://github.com/NonakaVal/lazy_review/tree/main).

##  Estrutura do Projeto
```
lazy_review/
├── documents/
│   └── .pdf
├── main.py/
├── crew_en.py/
├── crew_pt.py/
├── TranscriptVideoExtractor.py/
└── README.md
```

