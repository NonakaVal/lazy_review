# Criando resumos de estudos com IA

## Overview

##  Estrutura do Projeto
```
salva-tempo-aulas-youtube/
├── documents/
│   └── .pdf
├── main.py/
├── crew_en.py/
├── crew_pt.py/
├── TranscriptVideoExtractor.py/
└── README.md
```



## Requisitos
- Python 3.10 or higher
- An [OpenAI](https://platform.openai.com) API key
- (logo subirei o requirements.txt)

## Uso e Testes

### Extrair Transcrição
```python
python TranscriptVideoExtractor.py
```

Cógido simples que solicita a URL do vídeo que deseja extrair a transcrição, lembrando que para que possa ser resumido com `main.py` é necessário nomear o arquivo sempre com `.pdf` no final, criando o arquivo na pasta `transcripts/`.


### Gerando Resumos 
```python
python main.py
```
O programa irá procurar e listar os arquivos `.pdf` localizados na pasta `documents\`, permitindo digitar um valor correspondente ao arquivo desejado.
Também será necessário definir o `context_topic`, para garantir que os prompts definidos nos agentes e tarefas extraim apenas as informações desejadas.
Por fim será solicitado o nome da pasta que sera criada para receber os outputs específicos daquela execução.

### Meus Agentes e Tarefas.


#### Agentes

`topic_researcher` : _Especializado em extrair informações relevantes de aulas e palestras._

`academic_reviewer` : _Especializado em revisar e identificar métodos específicos apresentados em contextos acadêmicos._

`ref_specialist` : _Especializado em identificar e descrever websites e referências mencionadas._

`prof` : _Escrever um tutorial (guia) passo a passo detalhado para o projeto apresentado na aula'_

`research_writer` : _ Capaz de realizar pesquisas detalhadas e escrever documentos estruturados sobre métodos acadêmicos_

#### Tarefas

`list_topics_task` : _Listar todos os tópicos abordados_

`academic_review_task` : _Identificar as técnicas e métodos apresentados_

`website_list_task` : _Listar sites mencionados e outras referências_

`tutorial_write_task` : _Produzir um guia/aula_

`research_write_task` : _Com base nos materiais fornecidos pelos outros agentes, escrever um relatório estruturado de todo conteúdo_


### Resultados
Cada tarefa irá gerar um arquivo `.md` na pasta criada, com suas respectivas informações, segue alguns testes que realizei para extrair resumos de alguns artigos e vídeos.



