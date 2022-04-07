import { SlashCommandBuilder } from '@discordjs/builders';
import { ColorResolvable, MessageEmbed } from 'discord.js';
import { Command } from "../types/Command";
import * as config from '../config.json';
import fetch from 'node-fetch';

export const command: Command = {
    actions: [ 
        new SlashCommandBuilder()
            .setName("cat")
            .setDescription("Send a random cat image!"),
        new SlashCommandBuilder()
            .setName("dog")
            .setDescription("Send a random dog image!")
    ],
    exec: async (bot, intr) => {
        const apis: any = {
            cat: 'https://api.thecatapi.com/',
            dog: 'https://api.thedogapi.com/'
        }
        const names: any = {
            cat: 'Cat',
            dog: 'Dog'
        }
        const api = apis[intr.commandName]
        const name = names[intr.commandName]
        
        /* Make sure the API for this command exists */
        if (typeof api === 'undefined' || !api)
            throw 'No animal API for ' + intr.commandName

        /* Fetch animal from API */
        const response = await fetch(api + 'v1/images/search')
        if (!response.ok) { // Check for non-OK response
            console.warn('Got non-OK response from animal API!', response.status, api);

            await intr.reply({
                content: "Couldn't reach animal API :(",
                ephemeral: true // Only show to requesting user
            });

            return;
        }

        /* Handle response data */
        const data = await response.json();
        if (data.length == 0) { // Response JSON is an array, make sure we have at least 1 object in it
            console.warn('Got response with 0 animals from animal API!', data, api);

            await intr.reply({
                content: "Couldn't get an animal from the animal API :(",
                ephemeral: true
            });

            return;
        }

        // Prepare response data for sending
        const animal: any = data[0]
        const animalBreedNames: string[] = []
        animal.breeds.forEach((breed: any) => animalBreedNames.push(breed.name))

        /* Send animal! */
        await intr.reply({
            embeds: [
                new MessageEmbed()
                    .setTitle(name)
                    .setColor(config.embed_color as ColorResolvable)
                    .setImage(animal.url)
                    .setDescription(animalBreedNames.join(', '))
            ]
        })
    }
};
