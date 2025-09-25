# AYA Bancah Alexa Skill

Este projeto é um servidor Flask centralizador para a Skill Alexa "AYA Bancah". Ele recebe intents, responde com boas-vindas, analisa palavras-chave (ex: 'resumo'), envia mídia conforme o tipo de dispositivo (MP3 para Echo comum, MP4 para Echo Show) e possui fallback para texto de desenvolvimento.

## Estrutura
- aya_server.py: servidor Flask
- noticia.mp3: exemplo de mídia para Echo comum (placeholder)
- noticia.mp4: exemplo de mídia para Echo Show (placeholder)

## Como usar
1. Instale dependências: `pip install flask`
2. Execute o servidor: `python aya_server.py`
3. Endpoint principal: `/alexa/tool/aya_bancah`

## Exemplo de payload Alexa
```json
{
  "request": {
    "type": "IntentRequest",
    "intent": {
      "name": "NoticiaIntent",
      "slots": {
        "palavra": { "value": "resumo" }
      }
    },
    "dialogState": "COMPLETED"
  },
  "context": {
    "System": {
      "device": {
        "supportedInterfaces": {
          "VideoApp": {}
        }
      }
    }
  }
}
```

## Observações
- Os arquivos de mídia são exemplos e devem ser substituídos pelos reais.
- O endpoint centraliza a lógica e pode ser expandido conforme novas intents.
