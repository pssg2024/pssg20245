from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey'  # Necessário para usar flash messages

# Crie o diretório de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    query = request.args.get('q')
    if query:
        files = [f for f in files if query.lower() in f.lower()]

    return render_template('index.html', files=files)

@app.route('/delete', methods=['POST'])
def delete_file():
    password = request.form.get('password')
    filename = request.form.get('filename')
    if password == '230655':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'File {filename} deleted successfully.')
        else:
            flash(f'File {filename} not found.')
    else:
        flash('Incorrect password.')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == "__main__":
    app.run(debug=True)
