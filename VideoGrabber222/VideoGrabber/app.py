from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Platform-specific download page
@app.route('/download/<platform>')
def download_page(platform):
    valid_platforms = ['youtube', 'instagram', 'linkedin', 'other']
    if platform not in valid_platforms:
        return "Platform not supported", 404
    return render_template('download.html', platform=platform.capitalize())

# Documentation page
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

# Get available video formats
@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'})
    try:
        with YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {'format_id': f['format_id'], 'resolution': f.get('resolution', 'Audio only'), 'ext': f['ext']}
                for f in info.get('formats', []) if f.get('vcodec') != 'none' or f.get('acodec') != 'none'
            ]
            return jsonify({'formats': formats, 'title': info['title']})
    except Exception as e:
        return jsonify({'error': str(e)})

# Download video
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_id = request.form.get('format_id')
    if not url or not format_id:
        return jsonify({'error': 'Missing URL or format ID'})
    try:
        with YoutubeDL({'quiet': True, 'no_warnings': True, 'format': format_id}) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = f"{info['title']}.{info['ext']}"
            filename = ''.join(c for c in filename if c.isalnum() or c in '._- ')
            return jsonify({'video_url': info['url'], 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)