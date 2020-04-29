let feed= document.getElementById("feed");
let feedMessages = document.querySelector("#feed > div");
let writtingMessage = document.getElementById("message");
let submitButton = document.getElementById("submit");
let mapNumber = 0

function clearMessage() {
    writtingMessage.value = "";
}

function createPost(author, content) {
    let post = document.createElement("p");
    post.classList.add("post", author);
    if (author === "incoming") { // App input post as HTML
        post.innerHTML = content;
    } else { // User input post as text
        post.textContent = content;
    }

    feedMessages.appendChild(post);
    feed.scrollTop = feed.scrollHeight;
}

function createMap(content) {
    // Increment mapNUmber ofr unique ID
    mapNumber++;

    // Create a div for the map
    let mapDiv = document.createElement("div");
    mapDiv.id = "map-" + mapNumber;
    mapDiv.classList.add("post", "incoming", "map");

    // Send the div in the fedd
    feedMessages.appendChild(mapDiv);
    feed.scrollTop = feed.scrollHeight;

    // Create the map
    let map = new mapboxgl.Map({
        container: mapDiv.id, // Container ID
        style: "mapbox://styles/mapbox/streets-v10", // Map style to use
        center: content["center"],// Starting position [lng, lat]
        zoom: 14, // Starting zoom level
    });

    // Change map language for french
    let language = new MapboxLanguage({
        defaultLanguage: "fr"
    });
    map.addControl(language);

    // Add a marker to the map
    new mapboxgl.Marker() // initialize a new marker
      .setLngLat(content["center"]) // Marker [lng, lat] coordinates
      .addTo(map); // Add the marker to the map
}

function processUserInput() {
    // Get the user message
    let form = document.querySelector("#writing form")

    // Post the user input in the feed
    createPost("sent", form.querySelector("#message").value);

    // Remove the class "hidden" for the waiting message
    let waitingPost = document.getElementById("waiting");
    feedMessages.appendChild(waitingPost);
    waitingPost.classList.remove("hidden");
    feed.scrollTop = feed.scrollHeight;

    // Send the user input to "/process"
    fetch("/process", {
        method: "POST",
        body: new FormData(form)
    })
        .then(response => response.json())
        .then(result =>  {
            if (Object.keys(result).length === 0) { // Si le résultat est nul
                createPost("incoming", "Je suis un boloss je trouve pas");
            } else {
                if ("map" in result) {
                    createPost("incoming", result["map"]["place_name"]);
                    createMap(result["map"]);
                }
                if ("article" in result) {
                    let article = result["article"]["extract"];
                    let article_link = "<br />[<a target='_blank' rel='noreferrer noopener' href='" + result["article"]["url"] + "'>Lire la suite sur Wikipédia</a>]";
                    article = article + article_link
                    createPost("incoming", article);
                }
            }
            waitingPost.classList.add("hidden");
            feed.scrollTop = feed.scrollHeight;
        })
        .catch(error => console.log(error));

    // Clear the writing form
    clearMessage();
}

writtingMessage.addEventListener("keydown", event =>  {
    // Event for using <Ctrl> or <Meta> + <Enter> for carriage return and <Enter> to submit message
    if (event.key == "Enter" && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        writtingMessage.value += "\n";
        writtingMessage.scrollTop = writtingMessage.scrollHeight;
    } else if (event.key == "Enter" && writtingMessage.value) {
        event.preventDefault();
        processUserInput();
    }
});

submitButton.addEventListener("click", event => {
    event.preventDefault();
    if (writtingMessage.value) {
        processUserInput();
    }
});

// Execute Clear message in case the user refresh the page with a message already written
clearMessage();

// Ask yoda to say hello!
fetch("/hello", {
    method: "GET"
})
    .then(response => response.json())
    .then(result => {
        if ("bot_messages" in result) {
            for (message of result["bot_messages"]) {
                createPost("incoming", message);
            }
        }
    })
    .catch(error => console.log(error));
