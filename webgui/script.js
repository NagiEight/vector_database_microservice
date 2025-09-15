document.getElementById('addForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('addText').value;
    const metadata = document.getElementById('addMetadata').value;

    try {
        const response = await fetch('http://localhost:8000/vectors/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                texts: [text],
                metadata: [JSON.parse(metadata)]
            }),
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('addStatus').textContent = `Vector added successfully! ID: ${data.ids[0]}`;
        } else {
            document.getElementById('addStatus').textContent = `Error: ${data.detail}`;
        }
    } catch (error) {
        document.getElementById('addStatus').textContent = `Request failed: ${error.message}`;
    }
});

document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('searchQuery').value;
    const k = document.getElementById('k').value;

    try {
        const response = await fetch('http://localhost:8000/vectors/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                k: parseInt(k)
            }),
        });

        const data = await response.json();
        if (response.ok) {
            const results = data.results;
            let output = '';
            results.forEach(res => {
                const { text, distance, ...metadata } = res;
                output += `Text: ${text}\n`;
                output += `Distance: ${distance.toFixed(4)}\n`;
                output += `Metadata: ${JSON.stringify(metadata, null, 2)}\n`;
                output += '------------------------------------\n';
            });
            document.getElementById('searchResults').textContent = output;
        } else {
            document.getElementById('searchResults').textContent = `Error: ${data.detail}`;
        }
    } catch (error) {
        document.getElementById('searchResults').textContent = `Request failed: ${error.message}`;
    }
});