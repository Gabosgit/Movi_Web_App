const btn_description = document.getElementById('btn_description');
const btn_bio = document.getElementById('btn_bio');
const form_update = document.getElementById('form_update');
const form_review = document.getElementById('form_review');



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
                document.getElementById('birth').value = data.birth;
                document.getElementById('death').value = data.death;
            } catch (error) {
                console.error("Error:", error);
                document.getElementById('movie_description').textContent = "An error occurred.";
            }
});


form_update.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent standard form submission

  const formData = new FormData(form_update);
  const data = {};
  formData.forEach((value, key) => {
    data[key] = value;
  });

  fetch(route, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
      // Handle the response.
      if (data.response) {
        const myString = "The INFO movie has been successfully updated"; // The string you want to send
        const msgColor = "green"
        localStorage.setItem('myString', myString);
        localStorage.setItem('msg_color', "green");
        window.location.href = route_movie_info;
      } else {
        // Handle the failure case (e.g., display an error message)
        console.log(result.message);
      }
      //window.location.href = route_movie_info;
    })
    .catch(error => {
      console.error('Error:', error);
    });
});



