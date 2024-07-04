async function deleteMovie(api_id) {
    console.log("API ID:", api_id); // Log the API ID to verify it's correct
    try {
        const response = await fetch("/delete-movie", {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_id: api_id }), // Ensure the API ID is being sent
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            console.error('Server Error:', errorResponse);
        } else {
            // Redirect to the favorites page after deletion
            window.location.href = "/favorites";
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

