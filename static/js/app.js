const socket = io();

function generateUsername() {
    const adjectives = ["Cool", "Happy", "Smart", "Fast", "Brave"];
    const animals = ["Lion", "Tiger", "Bear", "Eagle", "Shark"];
    const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
    const animal = animals[Math.floor(Math.random() * animals.length)];
    return `${adjective}${animal}${Math.floor(Math.random() * 1000)}`;
}

const username = generateUsername();

const chatToggleButton = document.getElementById('chat-toggle-button');
const chatContainer = document.getElementById('chat-container');
const chatCloseButton = document.getElementById('chat-close-button');

chatToggleButton.addEventListener('click', () => {
    chatContainer.style.display = chatContainer.style.display === 'none' ? 'flex' : 'none';
});

chatCloseButton.addEventListener('click', () => {
    chatContainer.style.display = 'none';
});

document.getElementById('send-button').addEventListener('click', () => {
    const message = document.getElementById('message-input').value;
    socket.emit('message', { username, message });
    document.getElementById('message-input').value = '';
});

socket.on('message', (data) => {
    const li = document.createElement('li');
    li.textContent = `${data.username}: ${data.message}`;
    document.getElementById('messages').appendChild(li);
});

document.getElementById('search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const artist = document.getElementById('artist').value;
    const country = document.getElementById('country').value;

    const queryString = `/top-tracks?artist=${encodeURIComponent(artist)}&country=${encodeURIComponent(country)}`;

    const response = await fetch(queryString);
    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const tracks = await response.json();

        const trackList = document.getElementById('track-list');
        trackList.innerHTML = '';

        if (tracks.length === 0) {
            const div = document.createElement('div');
            div.className = 'track-item';
            div.textContent = 'No tracks found for this artist in the specified country.';
            trackList.appendChild(div);
        } else {
            tracks.forEach((track, index) => {
                const div = document.createElement('div');
                div.className = 'track-item';

                const trackNumber = document.createElement('div');
                trackNumber.className = 'track-number';
                trackNumber.textContent = `${index + 1}`;
                div.appendChild(trackNumber);

                const trackName = document.createElement('div');
                trackName.className = 'track-name';
                trackName.textContent = track.name;
                div.appendChild(trackName);

                if (track.album && track.album.images && track.album.images.length > 0) {
                    const albumCover = document.createElement('img');
                    albumCover.className = 'album-cover';
                    albumCover.src = track.album.images[0].url;
                    div.appendChild(albumCover);
                }

                if (track.preview_url) {
                    const audio = document.createElement('audio');
                    audio.src = track.preview_url;
                    audio.controls = true;
                    div.appendChild(audio);
                } else {
                    const noPreview = document.createElement('span');
                    noPreview.textContent = ' (Preview not available)';
                    div.appendChild(noPreview);
                }
                trackList.appendChild(div);
            });
        }
    }
});
