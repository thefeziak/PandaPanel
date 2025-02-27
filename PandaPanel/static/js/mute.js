let isMuted = JSON.parse(localStorage.getItem('isMuted')) || false;

const toggleMute = () => {
    const iframe = document.getElementById("youtubePlayer");
    const muteButton = document.getElementById("muteButton");

    if (iframe) {
        if (!isMuted) {
            iframe.contentWindow.postMessage('{"event":"command","func":"mute","args":""}', '*');
            muteButton.src = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Mute_Icon.svg";
        } else {
            iframe.contentWindow.postMessage('{"event":"command","func":"unMute","args":""}', '*');
            muteButton.src = "https://upload.wikimedia.org/wikipedia/commons/2/21/Speaker_Icon.svg";
        }
        isMuted = !isMuted;
        localStorage.setItem('isMuted', JSON.stringify(isMuted));
    }
};

const applyMuteState = () => {
    const iframe = document.getElementById("youtubePlayer");
    const muteButton = document.getElementById("muteButton");

    if (iframe) {
        if (isMuted) {
            iframe.contentWindow.postMessage('{"event":"command","func":"mute","args":""}', '*');
            muteButton.src = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Mute_Icon.svg";
        } else {
            iframe.contentWindow.postMessage('{"event":"command","func":"unMute","args":""}', '*');
            muteButton.src = "https://upload.wikimedia.org/wikipedia/commons/2/21/Speaker_Icon.svg";
        }
    }
};

document.getElementById("muteButton").addEventListener("click", toggleMute);
window.addEventListener("load", applyMuteState);