let feed= document.getElementById('feed');
let feedMessages = document.querySelector('#feed > div');
let writtingMessage = document.getElementById('message');
let submitButton = document.getElementById('submit');

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
        .then(response => response.text()) // Catch the response as text (temporary)
        .then(result => {                  // Use the result for creating posts
            if(result) {
                createPost('incoming', result);
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
