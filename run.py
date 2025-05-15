from app import create_app

# Criação da instância do app
app = create_app()

# Iniciando o servidor
if __name__ == "__main__":
    app.run(debug=True)