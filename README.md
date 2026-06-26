Phantom Matrículas
Sistema Acadêmico de Gerenciamento de Matrículas

1. Introdução

O Phantom Matrículas é um sistema desktop desenvolvido em Python com o objetivo de realizar o gerenciamento acadêmico de alunos, turmas e solicitações administrativas. O sistema foi construído utilizando a biblioteca Tkinter para a interface gráfica e MongoDB Atlas como banco de dados NoSQL para persistência das informações.

A aplicação permite que alunos realizem solicitações acadêmicas, enquanto coordenadores possuem acesso administrativo para gerenciamento das informações cadastradas.

2. Objetivos do Projeto

Objetivo Geral

Desenvolver uma aplicação desktop capaz de realizar o gerenciamento acadêmico de alunos e solicitações administrativas de maneira simples e intuitiva.

Objetivos Específicos
Realizar cadastro de alunos;
Gerenciar turmas acadêmicas;
Permitir solicitações realizadas pelos alunos;
Utilizar persistência de dados em banco NoSQL;
Aplicar conceitos de interface gráfica em Python.

3. Arquitetura do Sistema

O sistema foi desenvolvido seguindo uma estrutura funcional baseada em separação lógica de responsabilidades.

A aplicação é composta por:

Camada	                Responsabilidade

Interface gráfica	Interação com usuário
Regras de negócio	Validações e operações
Persistência	        Comunicação com MongoDB

4. Tecnologias Utilizadas

Tecnologia	Finalidade

Python	        Linguagem principal
Tkinter	        Interface gráfica
Pillow	        Manipulação de imagens
PyMongo	        Integração com MongoDB
MongoDB Atlas	Banco de dados em nuvem

5.Estrutura Funcional do Sistema

Área do Aluno

O aluno pode:

Solicitar troca de turma;
Solicitar remoção de turma;
Solicitar bolsa;
Solicitar alteração de nome.

Área do Coordenador

O coordenador pode:

Cadastrar alunos;
Visualizar listagem de alunos;
Atribuir turmas;
Remover alunos das turmas;
Aprovar ou recusar solicitações.
