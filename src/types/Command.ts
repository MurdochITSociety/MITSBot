import { SlashCommandBuilder } from "@discordjs/builders";
import { CommandInteraction } from "discord.js";
import Bot from '../Bot';

type Execute = (bot: Bot, interaction: CommandInteraction) => Promise<void>;

export interface Command {
    /**
     * Issue with using SlashCommandBuilder and sub commands.
     * Any addition of a sub command produces some error i cant seem to make sense of
     * Changed to 'any' as a temporary fix.
     */
    data: any;
    exec: Execute;
}