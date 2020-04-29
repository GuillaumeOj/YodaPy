class Post {
    constructor(feed) {
        this.content = "";
        this.feed = feed;
    }

    newPost(content, author) {
        this.content = content;

        this.post = document.createElement("p");
        this.post.classList.add("post");

        if (author == "user") {
            this.userPost();
        } else {
            this.botPost();
        }
        this.feed.write(this.post);
    }

    userPost() {
        this.post.classList.add("sent");
        this.post.textContent = this.content;
    }

    botPost() {
        this.post.classList.add("incoming");
        this.post.innerHTML = this.content;
    }
}
