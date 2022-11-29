import { SlashCommandBuilder } from '@discordjs/builders';
import { ColorResolvable, EmbedBuilder } from 'discord.js'; //changes from v13->v14
import axios from 'axios';
import { Command } from '../types/Command';
import * as config from '../config.json';

export const command: Command = {
    data: new SlashCommandBuilder()
        .setName("fact")
        .setDescription("Retrieves facts about different things.")
        
        .addSubcommand(sc => sc
            .setName("cat")
            .setDescription("Retrieves a cat fact.")
        )
        .addSubcommand(sc => sc
            .setName("java")
            .setDescription("Retrieves a java fact.")
        ),
    exec: async (bot, intr) => {
        /**
         * Something to do with ApplicationCommand type being shared between slash commands and context menu commands.
         * Context menus dont have subcommands, so having 'const sc = intr.options.getSubcommand()' produces and error
         * as sub commands may not exist
         */
        if(intr.isChatInputCommand()) {
            const sc = intr.options.getSubcommand();
            await getFact(sc)
            .then(async (val: string) => await intr.reply({
                embeds: [
                    new EmbedBuilder()
                        .setColor(config.embed_color as ColorResolvable)
                        .setTitle(`Here is a ${sc} fact!`)
                        .setDescription(val)
                ]
            }))
            .catch(async (err: Error) => {
                console.warn(`Error in Fact Command: ${err.message}`);

                await intr.reply({
                    content: `Couldn't retrieve a ${sc} fact :(`,
                    ephemeral: true
                });
            });
        }
        else {
            return;
        }
    }
};

async function getFact(subCommand: string): Promise<string> {
    switch (subCommand) {
        case "cat":
            return await axios.get("https://catfact.ninja/fact")
                .then(res => {
                    if (res.data.length == 0)
                        return Promise.reject(new Error("API returned length = 0"));

                    return Promise.resolve(res.data.fact)
                })
                .catch(err => Promise.reject(err));
        case "java":
            const entries = config.commands.fact.java.entries; // Our entries from config.json
            const randIndex = Math.floor(Math.random() * (entries.length) + 1) - 1; // Random entry index

            // If there are no entries in the config file
            if (!(entries.length > 0))
                return Promise.reject(new Error("No entries in configuration file"));

            return Promise.resolve(entries[randIndex]);
        default:
            return Promise.reject(new Error(`No option  \`${subCommand}\``));
    }
}
