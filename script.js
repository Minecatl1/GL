<script>
    fetch('game_list.json')
        .then(response => response.json())
        .then(games => {
            console.log('Fetched games:', games);  // Log games to console
            const gameList = document.getElementById('gameList');
            const gameIframe = document.getElementById('gameIframe');
            games.forEach(game => {
                const listItem = document.createElement('li');
                listItem.className = 'game-item';

                if (game.icon) {
                    const icon = document.createElement('img');
                    icon.src = game.icon;
                    icon.alt = `${game.name} icon`;
                    icon.className = 'game-icon';
                    listItem.appendChild(icon);
                }

                const text = document.createTextNode(game.name);
                listItem.appendChild(text);

                listItem.addEventListener('click', () => {
                    if (game.type === 'html') {
                        gameIframe.src = game.path;
                    } else if (game.type === 'web') {
                        gameIframe.src = game.url;
                    } else if (game.type === 'nes') {
                        fetch('/launch_nes', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ path: game.path })
                        })
                        .then(response => response.text())
                        .then(data => console.log(data))
                        .catch(error => console.error('Error launching NES game:', error));
                    } else if (game.type === 'xci') {
                        window.open(`ryujinx://load?path=${game.path}`, '_blank')  // Adjust this line to match Ryujinx URL scheme
                    }
                });

                gameList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching game list:', error));
</script>
