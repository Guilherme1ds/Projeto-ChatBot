# 🌿 FlorIA Chatbot

Desenvolvido por: Guilherme Henrique Bernardi e Gustavo Franco Pereira

> **"Semeando dados, colhendo resultados."**

A **FlorIA** é uma assistente virtual (chatbot) focada no universo botânico, jardinagem e agricultura. Representada pelo mascote de um robô jardineiro simpático, ela foi desenvolvida para ajudar amantes de plantas, paisagistas, jardineiros e agricultores a tirar dúvidas sobre cultivo, pragas, adubação e cuidados gerais com a flora.

---

## 🎯 Proposta do Sistema

O objetivo da FlorIA é ser o "dedo verde" digital do usuário. Através de uma interface amigável e acolhedora, o sistema une o design de um chat moderno a um motor de Inteligência Artificial preparado para dar conselhos sobre plantas.

Sob o capô, o projeto utiliza uma arquitetura **Cliente-Servidor (Frontend + Backend)** para garantir a segurança dos dados e das chaves de API:

* **No Frontend:** Uma interface limpa, responsiva e focada na usabilidade, onde o usuário pode perguntar desde *"Como cuidar de uma suculenta?"* até *"Como tratar fungos nas folhas do tomateiro?"*.
* **No Backend:** Um servidor em Python atuando como ponte de segurança. Ele recebe a dúvida do usuário, se comunica com a **API da Groq** (utilizando o avançado modelo Llama 3.1) e devolve a dica ou diagnóstico de forma rápida e precisa.
