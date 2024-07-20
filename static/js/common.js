async function addComment(postId) {
    const content = document.getElementById(`comment-${postId}`).value;
    try {
        const response = await fetch(`/posts/${postId}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });
        if (response.ok) {
            location.reload();
        } else {
            console.error('Failed to add comment');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function deletePost(postId) {
    fetch(`/posts/${postId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Post deleted successfully');
            location.reload();
        }
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.toggle-comments').forEach(button => {
        button.addEventListener('click', () => {
            const commentsSection = button.nextElementSibling;
            if (commentsSection.style.display === 'none') {
                commentsSection.style.display = 'block';
                button.textContent = 'Hide Comments';
            } else {
                commentsSection.style.display = 'none';
                button.textContent = 'Comments';
            }
        });
    });
});
