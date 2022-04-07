import Collection from "@discordjs/collection";
import { REST } from "@discordjs/rest";
import { Routes } from "discord-api-types/v10";
import { SlashCommandBuilder } from '@discordjs/builders';
import fs from "fs";
import path from "path";
import Bot from "../Bot";
import { Command } from "../types/Command";
import * as config from "../config.json";

export class CommandHandler {
    public commands: Collection<string, Command>;

    constructor() {
        this.commands = new Collection<string, Command>();
    }

    public async registerCommands(bot: Bot): Promise<void> {
        const rest = new REST({ version: '10' }).setToken(config.token);
        const commandsDir = path.join(__dirname, "..", "commands");
        const commandsFiles = fs.readdirSync(commandsDir).filter(f => f.endsWith(".ts"));

        /* Load all commands in src/commands/ */
        for (const file of commandsFiles) {
            const { command } = await import(`${commandsDir}/${file}`);

            if (!command)
                continue;

            command.actions.forEach((action: SlashCommandBuilder) => this.commands.set(action.name, command))
        }

        /* Prepare to send command action list to Discord */
        const body: any[] = []
        this.commands.forEach(command => {
            command.actions.forEach(action => body.push(action))
        })

        await rest
            .put(
                Routes.applicationGuildCommands(
                    config.applicationId,
                    config.server),
                { body })
            .then(() => console.log("Registered commands successfully!"))
            .catch((e) => console.log(e));
    }

    public async handleInteractions(bot: Bot): Promise<void> {
        bot.on('interactionCreate', async (intr) => {
            if (!intr.isCommand())
                return;

            if (!this.commands.has(intr.commandName))
                return;

            await this.commands.get(intr.commandName)?.exec(bot, intr);
        });
    }

}
