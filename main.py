from website import create_app

# Create application
app = create_app()

# run website locally
if __name__ == '__main__':
   app.run(debug=True)