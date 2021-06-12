function loadPosts() {
    return $.ajax('api/posts')
}

function renderPosts(posts) {

    const postsHtml = posts.map(
        post => `<b>Пост id:</b>
            <a href="posts/${post.id}">
            ${post.id}
            </a>
            <br>
            <b>Пост текст:</b>
            ${post.text}
            <br>`
    )

    return postsHtml.join("");
}

$(document).ready(async function () {
    const posts = await loadPosts();
    const html = renderPosts(posts.results);
    $('#posts').html(html);
})