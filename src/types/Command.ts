import { SlashCommandBuilder } from "@discordjs/builders";
import { CommandInteraction } from "discord.js";
import Bot from '../Bot';

type Execute = (bot: Bot, interaction: CommandInteraction) => Promise<void>;

export interface Command {
    actions: SlashCommandBuilder[];
    exec: Execute;
}
