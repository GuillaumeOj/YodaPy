class Feed {
    constructor (feed, waiting) {
        this.feed = feed;
        this.waiting = waiting;
        this.feedMessages = feed.querySelector("div");
    }

    write (content) {
        this.feedMessages.appendChild(content);
        this.scrollAuto();
    }

    waitOn () {
        this.feedMessages.appendChild(this.waiting);
        this.waiting.classList.remove("hidden");
        this.scrollAuto();
    }

    waitOff () {
        this.waiting.classList.add("hidden");
        this.scrollAuto();
    }

    scrollAuto() {
        this.feed.scrollTop = this.feed.scrollHeight;
    }
}
