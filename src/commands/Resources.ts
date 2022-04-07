import { SlashCommandBuilder } from '@discordjs/builders';
import { ColorResolvable } from 'discord.js';
import { Command } from "../types/Command";
import * as config from "../config.json";

const resourcesEmbed = {
    color: config.embed_color as ColorResolvable,
    title: "<:student:780271578608828437> Resources",
    fields: [
        {
            name: "<:book:780285717124743168> Studying",
            value: "\
                [myMurdoch Learning](https://moodleprod.murdoch.edu.au/my/)\n\
                [Murdoch Library](https://www.murdoch.edu.au/library)\n\
                [Murdoch Referencing](https://www.murdoch.edu.au/library/help-support/support-for-students/referencing)\n\
                [Study Resources](https://moodleprod.murdoch.edu.au/course/view.php?id=9416#section-6)\n\
                [Murdoch Bookshop](https://our.murdoch.edu.au/Bookshop/)\n\
                [Student Hub Booking](https://studenthub.libcal.com/)\
            ",
            inline: true
        },
        {
            name: "<:question:780285635021897729> Course Help",
            value: "\
                [Murdoch Handbook](https://handbook.murdoch.edu.au/)\n\
                [Dates and Timetables](https://timetables.murdoch.edu.au/)\n\
                [Course Plans](https://www.murdoch.edu.au/mymurdoch/support-advice/student-admin/enrolment/how-to-enrol/course-plans/)\n\
                [myMurdoch Advice](https://www.murdoch.edu.au/mymurdoch/support-advice/mymurdoch-advice)\n\
                [Academic Contacts](https://www.murdoch.edu.au/contacts/academic/)\
            ",
            inline: true
        },
        {
            name: '\u200b',
            value: '\u200b',
            inline: false
        },
        {
            name: "<:computer:780285373959634984> Student Software",
            value: "\
                [Azure Dev Tools](https://azureforeducation.microsoft.com/devtools)\n\
                [GitHub Developer Pack](https://education.github.com/pack)\n\
                [VMware Academy](https://e5.onthehub.com/WebStore/ProductsByMajorVersionList.aspx?ws=ef64204f-8ec4-de11-886d-0030487d8897&vsro=8)\
            ",
            inline: true
        },
        {
            name: "<:briefcase:780285263585738815> Jobs and Internships",
            value: "\
                [GradConnection](https://au.gradconnection.com/graduate-jobs/information-technology/)\n\
                [GradAustralia](https://gradaustralia.com.au/)\
            ",
            inline: true
        },
        {
            name: '\u200b',
            value: '\u200b',
            inline: false
        },
        {
            name: "<:person_raising_hand:780285082228228116> Support",
            value: "\
                [Murdoch Support Services](https://www.murdoch.edu.au/life-at-murdoch/support-services)\n\
                [Murdoch Counselling](https://www.murdoch.edu.au/counselling)\n\
                [Murdoch Doctor](http://www.murdoch.edu.au/Medical/Making-an-appointment/)\n\
                [Mental Health Helplines](https://www.healthdirect.gov.au/mental-health-helplines)\n\
                [Headspace](https://headspace.org.au/)\
            ",
            inline: true
        }
    ]
};

export const command: Command = {
    actions: [ new SlashCommandBuilder()
        .setName('resources')
        .setDescription("Prints a curated list of resources for students.") ],
    exec: async (bot, intr) => {
        await intr.reply({ embeds: [resourcesEmbed] });
    }
};
