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

        this.sayWait();

        fetch("/process", {
            method: "POST",
            body: formData,
            headers: this.HttpHeaders
        })
            .then(response => response.json())
            .then(result =>  {
                this.feed.waitOff();
                if (Object.keys(result).length === 0) { // Si le résultat est nul
                    this.posts.newPost("Je trouve pô !", "bot");
                } else {
                    if ("map" in result) {
                        this.posts.newPost(result["map"]["place_name"], "bot");
                        this.maps.createMap(result["map"]["center"]);
                    }
                    if ("article" in result) {
                        let article = result["article"]["extract"];
                        let article_link = "<br />[<a target='_blank' rel='noreferrer noopener' href='"
                            + result["article"]["url"] + "'>Lire la suite sur Wikipédia</a>]";
                        article = article + article_link
                        this.posts.newPost(article, "bot");
                    }
                }
            })
            .catch(error => {
                this.feed.waitOff()
                console.log(error)
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

    sayWait() {
        // Ask yoda to say wait!
        fetch("/wait", {
            method: "GET"
        })
            .then(response => response.json())
            .then(result => {
                if ("bot_messages" in result) {
                    for (message of result["bot_messages"]) {
                        this.posts.newPost(message, "bot");
                    }
                    this.feed.waitOn();
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
