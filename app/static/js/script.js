let feed= document.getElementById('feed');
let feedMessages = document.querySelector('#feed > div');
let writtingMessage = document.getElementById('message');
let submitButton = document.getElementById('submit');

function clearMessage() {
    writtingMessage.value = '';
}

function processUserInput() {
    let userMessage = {'author': 'sent', 'content': writtingMessage.value};
    let post = document.createElement('p');
    post.classList.add('post', userMessage['author']);
    post.textContent = userMessage['content'];
    feedMessages.appendChild(post);
    feed.scrollTop = feed.scrollHeight;
    clearMessage();
}

writtingMessage.addEventListener('keydown', function(event) {
    /* Event for using <Ctrl> or <Meta> + <Enter> for carriage return and <Enter> to submit message */
    if (event.key == 'Enter' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        writtingMessage.value += '\n';
        this.scrollTop = this.scrollHeight;
    } else if (event.key == 'Enter' && writtingMessage.value) {
        event.preventDefault();
        processUserInput();
    }
});

submitButton.addEventListener('click', function(event) {
    event.preventDefault();
    if (writtingMessage.value) {
        processUserInput();
    }
})

/* Execute Clear message in case the user refresh the page with a message already written */
clearMessage();