class Bot {
    constructor(feed, form, waiting) {
        this.feed = new Feed(feed, waiting);

        this.maps = new BotMap(this.feed);

        this.posts = new Post(this.feed);

        this.form = form;
        this.submitButton = this.form.querySelector("#submit");
        this.user_input = this.form.querySelector("#message");

        this.HttpHeaders = new Headers();
        this.HttpHeaders.append("Keep-Alive", "timeout=10");


        this.sayHello();
        this.clearForm();
    }

    clearForm () {
        this.user_input.value = "";
    }

    process() {
        this.posts.newPost(this.user_input.value, "user");

        let formData = new FormData(this.form);
        this.clearForm();

        this.feed.waitOn();

        fetch("/process", {
            method: "POST",
            body: formData,
            headers: this.HttpHeaders
        })
            .then(response => {
                this.feed.waitOff();
                let status_code = response.status;
                if (status_code == 200) {
                    return response.json();
                } else if (status_code == 204) {
                    throw new Error("Not found");
                } else {
                    throw new Error("Fatal error");
                }
            })
            .then(result =>  {
                if ("map" in result) {

                    let postMessage = result["map"]["bot_messages"][0];
                    postMessage += "\n";
                    postMessage += result["map"]["place_name"];

                    this.posts.newPost(postMessage, "bot");
                    this.maps.createMap(result["map"]["center"]);
                }
                if ("article" in result) {
                    let article = result["article"]["extract"];
                    let article_link = "<br />[<a target='_blank' rel='noreferrer noopener' href='"
                        + result["article"]["url"] + "'>Lire la suite sur Wikipédia</a>]";
                    article = article + article_link
                    this.posts.newPost(article, "bot");
                }
            })
            .catch(error => {
                if (error.message == "Not found") {
                    fetch("/not_found", {
                        method: "GET",
                        headers: this.HttpHeaders
                    })
                        .then(response => response.json())
                        .then(result => {
                            for (message of result["bot_messages"]) {
                                this.posts.newPost(message, "bot");
                            }
                        })
                        .catch(error => console.log(error));
                } else {
                    fetch("/error", {
                        method: "GET",
                        headers: this.HttpHeaders
                    })
                        .then(response => response.json())
                        .then(result => {
                            for (message of result["bot_messages"]) {
                                this.posts.newPost(message, "bot");
                            }
                        })
                        .catch(error => console.log(error));
                }
            });
    }

    sayHello() {
        // Ask yoda to say hello!
        fetch("/hello", {
            method: "GET"
        })
            .then(response => response.json())
            .then(result => {
                if ("bot_messages" in result) {
                    for (message of result["bot_messages"]) {
                        this.posts.newPost(message, "bot");
                    }
                }
            })
            .catch(error => console.log(error));
    }
}

let feed = document.getElementById("feed");
let form = document.getElementById("form");
let waiting = document.getElementById("waiting");

let bot = new Bot(feed, form, waiting);

bot.user_input.addEventListener("keydown", event =>  {
    // Event for using <Ctrl> or <Meta> + <Enter> for carriage return and <Enter> to submit message
    if (event.key == "Enter" && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        bot.user_input.value += "\n";
        bot.user_input.scrollTop = bot.user_input.scrollHeight;
    } else if (event.key == "Enter" && bot.user_input.value) {
        event.preventDefault();
        bot.process();
    }
});

bot.submitButton.addEventListener("click", event => {
    event.preventDefault();
    if (bot.user_input.value) {
        bot.process();
    }
});
