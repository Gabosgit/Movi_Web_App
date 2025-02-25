const btn_description = document.getElementById('btn_description');


const btn_bio = document.getElementById('btn_bio');


btn_description.addEventListener('click', async function() {
            try {
                const response = await fetch(route, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: 'description' })
                });
                const data = await response.json();
                document.getElementById('text_description').textContent = data.response;
            } catch (error) {
                console.error("Error:", error);
                document.getElementById('movie_description').textContent = "An error occurred.";
            }
});

btn_bio.addEventListener('click', async function() {
            try {
                const response = await fetch(route, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: 'bio' })
                });
                const data = await response.json();
                document.getElementById('text_bio').textContent = data.response;
                document.getElementById('birth').textContent = data.birth;
                document.getElementById('death').textContent = data.death;
            } catch (error) {
                console.error("Error:", error);
                document.getElementById('movie_description').textContent = "An error occurred.";
            }
});