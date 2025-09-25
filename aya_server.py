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
                'text': 'Bem-vindo à AYA Bancah! Me diga em poucas palavras quais notícias você gostaria de ouvir.'
            },
            'shouldEndSession': False
        }
        return jsonify(response)

    # Intents
    intent = data.get('request', {}).get('intent', {})
    palavra = intent.get('slots', {}).get('palavra', {}).get('value', '').lower()
    device = data.get('context', {}).get('System', {}).get('device', {}).get('supportedInterfaces', {})

    # Se pediu resumo
    if palavra == 'resumo':
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
        else:
            # Echo comum: envia áudio
            response['response'] = {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': f'<speak>Ouça o resumo: <audio src="{request.url_root}static/noticia.mp3"/></speak>'
                },
                'shouldEndSession': True
            }
        return jsonify(response)

    # Fallback
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
