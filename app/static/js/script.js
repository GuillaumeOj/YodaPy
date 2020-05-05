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
		window.scrollTop = 0;
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
                if (status_code < 300) {
                    return response.json();
                } else {
                    throw new Error("Fatal error");
                }
            })
            .then(result =>  {
                if ("bot_error" in result) {
                    this.posts.newPost(result["bot_error"], "bot");
                }
                if ("bot_message" in result) {
                    this.posts.newPost(result["bot_message"], "bot");
                }
                if ("map" in result) {
                    let postMessage = result["map"]["bot_message"];
                    postMessage += "\n";
                    postMessage += result["map"]["place_name_fr"];

                    this.posts.newPost(postMessage, "bot");
                    this.maps.createMap(result["map"]["latitude"], result["map"]["longitude"]);
                }
                if ("article" in result) {
                    let article = result["article"]["bot_message"];
                    article += "\n";
                    article += result["article"]["extract"];
                    article += "<br />[<a target='_blank' rel='noreferrer noopener' href='"
                        + result["article"]["url"] + "'>Lire la suite sur Wikipédia</a>]";

                    this.posts.newPost(article, "bot");
                }
            })
            .catch(error => {
                fetch("/error", {
                    method: "GET",
                    headers: this.HttpHeaders
                })
                    .then(response => response.json())
                    .then(result => {
                        this.posts.newPost(result["bot_error"], "bot");
                    })
                    .catch(error => console.log(error));
            });
    }

    sayHello() {
        // Ask yoda to say hello!
        fetch("/hello", {
            method: "GET"
        })
            .then(response => response.json())
            .then(result => {
                if ("bot_message" in result) {
                    this.posts.newPost(result["bot_message"], "bot");
                }
            })
            .catch(error => console.log(error));
    }
}

let feed = document.getElementById("feed");
let form = document.getElementById("form");
let waiting = document.getElementById("waiting");

// Init the bot !
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
