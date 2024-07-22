const Discord = require('discord.js');

const ytdl = require('ytdl-core');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');

const client = new Discord.Client();

// Define your slash commands
const commands = [
    {
        name: 'play',
        description: 'Plays a song',
        options: [{
            name: 'song',
            type: 'STRING',
            description: 'The URL of the song to play',
            required: true,
        }],
    },
];

// Register your slash commands
const rest = new REST({ version: '9' }).setToken('MTI0MzkzODY0NjMwNjg1MzAwMQ.Gi-PpC.00njnBrxrytx0oE6FsHvDkrB-yJ_-afPtnMsf8');
rest.put(Routes.applicationGuildCommands('1243938646306853001', '1234201995787763732'), { body: commands })
    .then(() => console.log('Successfully registered application commands.'))
    .catch(console.error);

client.once('ready', () => {
    console.log('Ready!');
});

client.once('reconnecting', () => {
    console.log('Reconnecting!');
});

client.once('disconnect', () => {
    console.log('Disconnect!');
});

client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;

    const { commandName } = interaction;

    if (commandName === 'play') {
        if (interaction.member.voice.channel) {
            const connection = await interaction.member.voice.channel.join();

            const song = interaction.options.getString('song');
            const dispatcher = connection.play(ytdl(song, { filter: 'audioonly' }));

            dispatcher.on('start', () => {
                interaction.reply('Playing...');
            });

            dispatcher.on('finish', () => {
                interaction.followUp('Finished playing!');
                connection.disconnect();
            });

        } else {
            interaction.reply('You need to join a voice channel first!');
        }
    }
});

client.login('MTI0MzkzODY0NjMwNjg1MzAwMQ.Gi-PpC.00njnBrxrytx0oE6FsHvDkrB-yJ_-afPtnMsf8');

