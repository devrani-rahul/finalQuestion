document.getElementById('generate-btn').addEventListener('click', function() {
    const topic = document.getElementById('topic').value;
    if (topic) {
        fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: topic })
        })
        .then(response => response.json())
        .then(data => {
            const questionList = document.getElementById('question-list');
            questionList.innerHTML = '';  // Clear previous questions
            if (data.questions && data.questions.length > 0) {
                data.questions.forEach((question, index) => {
                    const p = document.createElement('p');
                    p.textContent = `Q${index + 1}: ${question}`;
                    questionList.appendChild(p);
                });
            } else {
                questionList.textContent = 'Error: No questions generated.';
            }
        });
    } else {
        alert("Please enter a topic.");
    }
});
