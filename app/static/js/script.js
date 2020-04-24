let feed= document.getElementById('feed');
let feedMessages = document.querySelector('#feed > div');
let writtingMessage = document.getElementById('message');
let submitButton = document.getElementById('submit');
let mapNumber = 0

function clearMessage() {
    writtingMessage.value = '';
}

function createPost(author, content) {
    let post = document.createElement('p');
    post.classList.add('post', author);
    post.textContent = content;

    feedMessages.appendChild(post);
    feed.scrollTop = feed.scrollHeight;
}

function createMap(content) {
    // Increment mapNUmber ofr unique ID
    mapNumber++;
    // Create a div for the map
    let mapDiv = document.createElement('div');
    mapDiv.id = 'map-' + mapNumber;
    mapDiv.classList.add('post', 'incoming', 'map');

    // Send the div in the fedd
    feedMessages.appendChild(mapDiv);
    feed.scrollTop = feed.scrollHeight;

    // Create the map
    let map = new mapboxgl.Map({
        container: mapDiv.id, // Container ID
        style: 'mapbox://styles/mapbox/streets-v10', // Map style to use
        center: content['center'],// Starting position [lng, lat]
        zoom: 14, // Starting zoom level
    });
    // Change map language for french
    let language = new MapboxLanguage({
        defaultLanguage: 'fr'
    });
    map.addControl(language);
    // Add a marker to the map
    new mapboxgl.Marker() // initialize a new marker
      .setLngLat(content['center']) // Marker [lng, lat] coordinates
      .addTo(map); // Add the marker to the map
}

function processUserInput() {
    // Get the user message
    let form = document.querySelector('#writing form')

    // Create a post for the feed
    createPost('sent', form.querySelector('#message').value);

    // Write a waiting message
    feedMessages.appendChild(document.getElementById('waiting'));

    // Remove the class 'hidden' for the waiting message
    let waitingPost = document.getElementById('waiting');
    waitingPost.classList.remove('hidden');

    // Send the message to '/process'
    fetch('/process', {
        method: "POST",
        body: new FormData(form)
    })
        .then(response => response.json()) // Catch the response as text (temporary)
        .then(result => {                  // Use the result for creating posts
            if(result["status_code"] < 400) {
                let content = result["content"]
                createPost('incoming', content["place_name"]);
                createMap(content)
            } else {
                createPost('incoming', 'Je suis un boloss je trouve pas');
            }
            waitingPost.classList.add('hidden');
        })
        .catch(error => console.log(error));

    // Clear the writing form
    clearMessage();
}

writtingMessage.addEventListener('keydown', event =>  {
    // Event for using <Ctrl> or <Meta> + <Enter> for carriage return and <Enter> to submit message
    if (event.key == 'Enter' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        writtingMessage.value += '\n';
        this.scrollTop = this.scrollHeight;
    } else if (event.key == 'Enter' && writtingMessage.value) {
        event.preventDefault();
        processUserInput();
    }
});

submitButton.addEventListener('click', event => {
    event.preventDefault();
    if (writtingMessage.value) {
        processUserInput();
    }
});

// Execute Clear message in case the user refresh the page with a message already written
clearMessage();
