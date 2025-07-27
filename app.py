from integrated_server import app, socketio

# Para Vercel, usamos apenas o app Flask sem socketio.run()
if __name__ == '__main__':
    # No Vercel, não executamos socketio.run() diretamente
    pass

# Exporta a aplicação para o Vercel
application = app
