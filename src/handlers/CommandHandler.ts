import Bot from "../Bot";
import { Collection } from "@discordjs/collection";
import { REST } from "@discordjs/rest";
import { Routes } from "discord-api-types/v10";
import { Command } from "../types/Command";
import { readdir } from "fs/promises"
import { join } from "path";
import * as config from "../config.json";

export class CommandHandler {
    public commands: Collection<string, Command>;

    constructor() {
        this.commands = new Collection<string, Command>();
    }

    public async importCommands(commandsDir: string): Promise<Command[]> {
        const directory = await readdir(commandsDir)
        const files = directory.filter(file => file.endsWith(".ts"))

        return Promise.all(files.map(async file => {
            const script = file.slice(0, -3) // remove .ts from filename for script name 
            const commands = await import(join(commandsDir, file))

            if (!commands)
                return;

            // Check for class type command
            if (typeof commands[script] === 'function') {
                const instance = new commands[script]()
                return instance
            }

            // Check for object type command
            if (typeof commands['command'] === 'object') {
                return commands['command']
            }
        }))
    }

    public async registerCommands(bot: Bot): Promise<void> {
        const rest = new REST({ version: '10' }).setToken(config.tokens.discord_bot);

        // Import all commands from commands folder
        const commands = await this.importCommands(join(__dirname, "..", "commands"));

        // Register commands
        commands.forEach(command => {
            this.commands.set(command.data.name, command);
        });

        // Send command info to Discord
        await rest
            .put(
                Routes.applicationGuildCommands(
                    config.applicationId,
                    config.server),
                { body: Array.from(this.commands.values()).map(v => v.data.toJSON()) })
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