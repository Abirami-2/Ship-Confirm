document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var fileInput = document.getElementById('file-input');
    var formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          var resultDiv = document.getElementById('result');
          if (data.error) {
              resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
          } else {
              if (data.duplicates.length > 0) {
                  resultDiv.innerHTML = `<p>Duplicate HUs found: ${data.duplicates.join(', ')}</p>`;
              } else {
                  resultDiv.innerHTML = '<p>No duplicates found.</p>';
              }
          }
      }).catch(error => {
          console.error('Error:', error);
      });
});
