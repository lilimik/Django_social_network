async function loadPosts() {
    const res = fetch('api/posts');
    return await res.json();
}

function renderPosts(posts) {

    const postsHtml = posts.map(
        post => `<b>Пост id:</b>
            ${post.id}
            <br>
            <b>Пост текст:</b>
            ${post.text}
            <br>`
    )

    return postsHtml.join("");
}

document.addEventListener('DOMContentLoaded', async function () {
    const posts = await loadPosts();
    const html = renderPosts(posts.results);
    const postsElement = document.querySelector("#posts")
    postsElement.innerHTML = html;
});
