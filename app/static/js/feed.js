class Feed {
    constructor (feed, waiting) {
        this.feed = feed;
        this.waiting = waiting;
        this.feedMessages = feed.querySelector("div");
    }

    // Write a content in the feed
    write (content) {
        this.feedMessages.appendChild(content);
        this.scrollAuto();
    }

    // Display the waiting spin
    waitOn () {
        this.feedMessages.appendChild(this.waiting);
        this.waiting.classList.remove("hidden");
        this.scrollAuto();
    }

    // Shut down the waiting spin
    waitOff () {
        this.waiting.classList.add("hidden");
        this.scrollAuto();
    }

    // Scroll the feed down
    scrollAuto() {
        this.feed.scrollTop = this.feed.scrollHeight;
    }
}
