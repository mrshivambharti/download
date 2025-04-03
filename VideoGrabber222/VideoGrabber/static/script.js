document.getElementById('url-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const formatsDiv = document.getElementById('formats');
    const status = document.getElementById('status');
    status.textContent = 'Fetching formats...';
    formatsDiv.innerHTML = '';

    fetch('/get_formats', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'url=' + encodeURIComponent(url)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            status.textContent = 'Error: ' + data.error;
        } else {
            status.textContent = '';
            data.formats.forEach(f => {
                const button = document.createElement('button');
                button.textContent = `${f.resolution} (${f.ext})`;
                button.onclick = () => downloadVideo(url, f.format_id, data.title);
                formatsDiv.appendChild(button);
            });
        }
    })
    .catch(error => {
        status.textContent = 'Error: ' + error.message;
    });
});

function downloadVideo(url, format_id, title) {
    fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `url=${encodeURIComponent(url)}&format_id=${encodeURIComponent(format_id)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('status').textContent = 'Error: ' + data.error;
        } else {
            const a = document.createElement('a');
            a.href = data.video_url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            document.getElementById('status').textContent = 'Download started';
        }
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Error: ' + error.message;
    });
}