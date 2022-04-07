import { SlashCommandBuilder } from '@discordjs/builders';
import { Command } from "../types/Command";

export const command: Command = {
    actions: [ new SlashCommandBuilder()
        .setName("ping")
        .setDescription("Pong!") ],
    exec: async (bot, intr) => {
        await intr.reply({
            content: `:ping_pong: ${bot.ws.ping}ms`,
            ephemeral: true
        });
    }
};
