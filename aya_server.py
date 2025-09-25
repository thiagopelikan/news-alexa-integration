from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Servir arquivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/alexa/tool/aya_bancah', methods=['POST'])
def aya_bancah():
    data = request.get_json()
    response = {}
    # Boas-vindas
    if data.get('request', {}).get('type') == 'LaunchRequest':
        response['response'] = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Bem-vindo à AYA Bancah! Me diga em poucas palavras quais notícias gostaria de ouvir.'
            },
            'shouldEndSession': False
        }
        return jsonify(response)

    # Intents
    intent = data.get('request', {}).get('intent', {})
    query = intent.get('slots', {}).get('query', {}).get('value', '').lower()
    device = data.get('context', {}).get('System', {}).get('device', {}).get('supportedInterfaces', {})

    # Se mencionou 'resumo' nas palavras ditas
    if 'resumo' in query:
        if 'VideoApp' in device:
            # Echo Show: envia vídeo
            response['response'] = {
                'directives': [{
                    'type': 'VideoApp.Launch',
                    'videoItem': {
                        'source': request.url_root + 'static/noticia.mp4',
                        'metadata': {
                            'title': 'Resumo em vídeo',
                            'subtitle': 'Notícia em vídeo para Echo Show'
                        }
                    }
                }],
                'shouldEndSession': True
            }
            return jsonify(response)
        elif device:
            # Echo comum: envia áudio
            response['response'] = {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': f'<speak>Ouça o resumo: <audio src="{request.url_root}static/noticia.mp3"/></speak>'
                },
                'shouldEndSession': True
            }
            return jsonify(response)
        else:
            # Nenhum suporte a vídeo/áudio: retorna transcrição
            texto_resumo = (
                'Dembélé. Ousmane Dembélé foi eleito o melhor jogador do mundo da temporada ao conquistar a Bola de Ouro na segunda-feira, '
                'em uma noite de triunfo para seu clube, o Paris Saint-Germain. Aitana Bommati. '
                'Aitana Bommati, do Barcelona, vencedora em série de troféus, levou o Prêmio Feminino. '
                'Dembélé, atacante francês de 28 anos, precisou de tempo e da orientação do técnico do PSG, Luiz Henrique, para alcançar seu potencial. '
                'Na temporada passada, ele foi o destaque do clube da capital francesa, rumo ao seu primeiro título da Liga dos Campeões. '
                'Dembélé se tornou o sexto francês a erguer o Prêmio. '
                'Ele superou o espanhol e atacante do Barcelona, Lamine Yamal, com seu companheiro de PSG, Vitinha, ficando em terceiro lugar. '
                'A espanhola Bommati, eleita jogadora da temporada na Liga dos Campeões, conquistou a Bola de Ouro pela terceira vez consecutiva.'
            )
            response['response'] = {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': texto_resumo
                },
                'shouldEndSession': True
            }
            return jsonify(response)

    # Fallback padrão para outros casos
    response['response'] = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Desculpe, ainda estamos desenvolvendo esta funcionalidade.'
        },
        'shouldEndSession': True
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
