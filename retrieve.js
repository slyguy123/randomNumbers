function downloadFile(url, filename) {
  fetch(url)
    .then(response => response.blob())
    .then(blob => {
      // Create a temporary URL for the blob
      const blobUrl = URL.createObjectURL(blob);

      // Create a link element
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = filename;

      // Programmatically trigger the download
      link.click();

      // Clean up the temporary URL
      URL.revokeObjectURL(blobUrl);
    })
    .catch(error => {
      // Handle any errors that occurred during retrieval
      console.error(error);
    });
}

// Usage
downloadFile('https://example.com/file.pdf', 'myfile.pdf');
