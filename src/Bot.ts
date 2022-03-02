import { Client, Intents } from "discord.js";
import { CommandHandler } from "./handlers/CommandHandler";
import * as config from "./config.json";

export default class Bot extends Client {
    public commandHandler: CommandHandler;

    constructor() {
        super({
            intents: [Intents.FLAGS.GUILDS]
        });

        this.commandHandler = new CommandHandler();
    }

    public async start(): Promise<void> {
        try {
            this.commandHandler.registerCommands(this);
            this.commandHandler.handleInteractions(this);
            await this.login(config.token)
                .then(() => console.log(`Logged in as ${this.application?.client.user?.username}`));
        } catch (e) {
            console.error(e);
        }
    }
}
