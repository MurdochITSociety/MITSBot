import { SlashCommandBuilder } from '@discordjs/builders';
import { ColorResolvable, AttachmentBuilder, EmbedBuilder } from 'discord.js'; //v13->v14
const fetch = require('node-fetch'); //update in node-fetch removed the ability to import it or something
import { join } from 'path';
import { readdir } from 'fs/promises';
import { Command } from '../types/Command';
import * as config from '../config.json';

export const command: Command = {
    data: new SlashCommandBuilder()
        .setName("image")
        .setDescription("Retrieves images.")
        .addSubcommand(sc => sc
            .setName("animal")
            .setDescription("Retrieves an image of the chosen animal.")
            .addStringOption(o => {
                // Add the fixed categories.
                o.addChoices( //v14 seems to have changed formatting for this
                    { name: 'cats', value: 'cats'},
                    { name: 'dogs', value: 'dogs'}
                );

                // Add the other categories, loaded from the configuration file.
                config.commands.image.animals.choices
                    .forEach(i => o.addChoices({ name: i, value: i }));

                return o
                    .setName("choice")
                    .setDescription("Chosen animal.")
                    .setRequired(true)
            })
            .addBooleanOption(b => b
                .setName("gif")
                .setDescription("If true, return a gif instead")
            )
        )
        .addSubcommand(sc => sc
            .setName("harold")
            .setDescription("Retrieves a picture of András Arató.")
        ),
    exec: async (bot, intr) => {
        /**
         * Something to do with ApplicationCommand type being shared between slash commands and context menu commands.
         * Context menus dont have subcommands, so having 'const sc = intr.options.getSubcommand()' produces and error
         * as sub commands may not exist
         */
        if(intr.isChatInputCommand()) {
            switch (intr.options.getSubcommand()) {
                case "animal":
                    const choice = intr.options.getString("choice");
                    const isGif = intr.options.getBoolean("gif");
    
                    await fetchAnimal(choice, isGif)
                        .then(async (url: string) => await intr.reply({
                            embeds: [
                                new EmbedBuilder()
                                    .setColor(config.embed_color as ColorResolvable)
                                    .setImage(`${url}`)
                                    .setTitle(`Here is a ${choice}!`)
                            ]
                        }))
                        .catch(async (err: Error) => {
                            console.warn(`Error in Image command: ${err.message}`);
    
                            await intr.reply({
                                content: `Couldn't retrieve an image of a ${choice} :(`,
                                ephemeral: true
                            });
                        });
                    break;
    
                case "harold":
                    // Relative directory path.
                    const dirPath = join(__dirname, "..", config.commands.image.harold.images_dir);
                    const files = await readdir(dirPath);
    
                    if (files.length == 0) {
                        console.warn("Error in Image command: No images of harold were found in the intended directory.");
    
                        await intr.reply({
                            content: "Couldn't retrieve an image of Harold :(",
                            ephemeral: true
                        });
                        break;
                    }
    
                    // Picked at random between 1 and `files.length`.
                    const fileName = files[Math.floor(Math.random() * ((files.length - 1) + 1) + 0)];
                    const attachment = new AttachmentBuilder(join(dirPath, fileName), {name: fileName});
    
                    await intr.reply({
                        embeds: [
                            new EmbedBuilder()
                                .setColor(config.embed_color as ColorResolvable)
                                .setImage(`attachment://${attachment.name}`)
                                .setTitle(`Here's Harold!`)
                        ],
                        files: [attachment]
                    });
                    break;
            }
        }
    }
};

// Searches for the specified term, and if content is found, return it's URL.
// imageType can be "Photo", or "AnimatedGif".
async function fetchRandomBingImage(searchTerm: string, imageType: string): Promise<string> {
    const randomPage = Math.floor(Math.random() * (200 - 0) + 0);
    const randomEntry = Math.floor(Math.random() * (35 - 0) + 0); // Bing's default `count` is 35

    // Form parameters
    const params = new URLSearchParams({
        "imageType": imageType,
        "offset": `${randomPage}`,
        "q": searchTerm + config.commands.image.animals.filter,
        "safeSearch": "Strict"
    });

    // Request headers
    const headers = {
        "Ocp-Apim-Subscription-Key": config.tokens.bing_image_api
    };

    return await fetch("https://api.bing.microsoft.com/v7.0/images/search?" + params.toString(),
        {
            headers: headers,
            method: 'GET'
        })
        .then(async (res: any) => {
            const data: any = await res.json(); //man i wish i knew why this works

            if (data.length == 0)
                throw Error("JSON body length is 0");

            if (data.value[randomEntry - 1].contentUrl.length == 0)
                throw Error("`contentUrl` length is 0");

            return data.value[randomEntry - 1].contentUrl;
        });
}

// For specific choices, we want to use the elected API's, and for everything
// else we want to use Bing's image search API.
async function fetchAnimal(choice: string | null, isGif: boolean | null): Promise<string> {
    const imageType = isGif ? "AnimatedGif" : "Photo";

    if (typeof choice !== 'string')
        return Promise.reject(new Error("`choice` is not of type string."));

    switch (choice) {
        // These two options use two APIs that have the same JSON output.
        case "cat":
        case "dog":
            // If a gif is requested, then use the Bing image search API.
            if (isGif)
                return fetchRandomBingImage(choice, imageType);

            // The URL is the same for both, minus the actual word for
            // either "cat" or "dog" in the domain name.
            return await fetch(`https://api.the${choice}api.com/v1/images/search`, { method: 'GET' })
                .then(async (res: any) => {
                    const data: any = await res.json();

                    if (data[0].length == 0)
                        throw Error("JSON body length is 0");

                    if (data[0].url.length == 0)
                        throw Error("`url` length is 0");

                    return data[0].url;
                });

        // For every other choice, use the Bing image search API.
        default:
            return fetchRandomBingImage(choice, imageType);
    }
}
