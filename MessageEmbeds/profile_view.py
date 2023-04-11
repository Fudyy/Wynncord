import discord.ui
from discord import Embed
from discord.utils import format_dt, escape_markdown

from WynnAPI.players import Player

rank_color = {
    'Player': 0xc9c9c9,  # Gray
    'VIP': 0x25a22d,  # Green
    'VIP+': 0x00fbff,  # Aqua
    'HERO': 0x9000ff,  # Purple
    'CHAMPION': 0xfbff05,  # Yellow
    'Media': 0xff00ff,  # Pink
    'Moderator': 0xff4d00,  # Orange
    'Game Master': 0x0098a3,  # Cyan
    'CMD': 0x0098a3,  # Cyan
    'Item': 0x0098a3,  # Cyan
    'Builder': 0x0098a3,  # Cyan
    'Hybrid': 0x0098a3,  # Cyan
    'Music': 0x0098a3,  # Cyan
    'WebDev': 0xff0000,  # Red
    'Administrator': 0xff0000  # Red
}


def get_rank_info(player: Player):
    """Gets the rank and the color of a player in a simple way"""
    if player.rank == 'Player' and player.meta.tag['value']:
        rank = player.meta.tag['value']
    elif player.rank == 'Player' and not player.meta.tag['value']:
        rank = 'Player'
    else:
        rank = player.rank

    color = rank_color[rank]

    return rank, color


def profile_embed_constructor(player: Player, rank: str, color: int):
    """
    Construct the profile embed for the given player (used in profile View)
    """
    embed = Embed(title=f"{escape_markdown(player.username)}", color=color,
                  url=f"https://wynncraft.com/stats/player/{player.username}")
    embed.set_thumbnail(url=f"https://mc-heads.net/head/{player.username}/left")
    embed.set_author(name="Wynncraft profile for:", icon_url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")

    # Check if the player is online
    if not player.meta.is_online:
        embed.add_field(name="Status:", value="🔴 Offline", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Last seen:", value=format_dt(player.meta.last_join, 'R'), inline=True)
    else:
        embed.add_field(name="Status:", value="🟢 Online", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Server:", value=player.meta.online_world)

    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="", value="====✴️====", inline=True)
    embed.add_field(name="", value="", inline=True)

    embed.add_field(name="Rank:", value=f"{rank.capitalize()}", inline=False)

    # Check if the player has a guild
    if player.guild['name']:
        embed.add_field(name="Guild:", value=f"{player.guild['name']}", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Guild rank:", value=f"{player.guild['rank'].capitalize()}", inline=True)

    embed.add_field(name="Total level:", value=f"{player.global_stats.total_level['combined']}", inline=True)
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="First join:", value=f"{format_dt(player.meta.first_join, 'f')}", inline=True)
    embed.set_footer(text="Check the characters! ↓")

    return embed


def character_embed_constructor(player: Player, color: int):
    """
    Construct the characters embed for the given player (used in profile View)
    """
    embed_list = []

    characters = sorted(player.characters, key=lambda c: c.professions['combat']['level'], reverse=True)

    character_types = {
        'HUNTER': 'archer',
        'DARKWIZARD': 'mage',
        'SKYSEER': 'shaman',
        'NINJA': 'assassin',
        'KNIGHT': 'warrior'
    }

    def get_character_image(character_type: str):
        # Made this for vip classes not having an icon
        if character_type in character_types:
            return f"https://cdn.wynncraft.com/nextgen/classes/icons/artboards/{character_types[character_type]}.webp"
        return f"https://cdn.wynncraft.com/nextgen/classes/icons/artboards/{character_type.lower()}.webp"

    index = 1
    for character in characters:
        # yeah, im getting the images from the wynn cdn, im sorry Nepmia ;w;
        embed = Embed(title=f"{escape_markdown(player.username)}", color=color,
                      url=f"https://wynncraft.com/stats/player/{player.username}")
        embed.set_thumbnail(url=get_character_image(character.type))
        embed.set_author(name="Wynncraft character for:",
                         icon_url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")

        embed.add_field(name="💎 Class:", value=f'{character.type.capitalize()}', inline=True)
        embed.add_field(name="⚔️ Combat Level:", value=f"{character.professions['combat']['level']}", inline=True)
        embed.add_field(name="💠 Logins:", value=f"{character.logins}", inline=True)

        embed.add_field(name="===============", value="", inline=True)
        embed.add_field(name="✨ Gathering profs ✨", value="", inline=True)
        embed.add_field(name="===============", value="", inline=True)

        embed.add_field(name="<:woodcutting:1094701633339924490> Woodcutting:",
                        value=f"{character.professions['woodcutting']['level']}", inline=True)
        embed.add_field(name="<:mining:1094701617938432161> Mining",
                        value=f"{character.professions['mining']['level']}", inline=True)
        embed.add_field(name="<:farming:1094701609675657368> Farming",
                        value=f"{character.professions['farming']['level']}", inline=True)
        embed.add_field(name="<:fishing:1094701612766871592> Fishing",
                        value=f"{character.professions['fishing']['level']}", inline=True)

        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="===============", value="", inline=True)
        embed.add_field(name="🛠️ Crafting profs 🛠️", value="", inline=True)
        embed.add_field(name="===============", value="", inline=True)

        embed.add_field(name="<:armouring:1093765660355608606> Armouring",
                        value=f"{character.professions['armouring']['level']}", inline=True)
        embed.add_field(name="<:tailoring:1093765680727326801> Tailoring",
                        value=f"{character.professions['tailoring']['level']}", inline=True)
        embed.add_field(name="<:weaponsmithing:1093765683407499294> Weaponsmithing",
                        value=f"{character.professions['weaponsmithing']['level']}", inline=True)
        embed.add_field(name="<:woodworking:1094701636565340170> Woodworking",
                        value=f"{character.professions['woodworking']['level']}", inline=True)
        embed.add_field(name="<:jeweling:1093765672284192858> Jeweling",
                        value=f"{character.professions['jeweling']['level']}", inline=True)
        embed.add_field(name="<:alchemism:1093765658623356968> Alchemism",
                        value=f"{character.professions['alchemism']['level']}", inline=True)
        embed.add_field(name="<:scribing:1093765677657100368> Scribing",
                        value=f"{character.professions['scribing']['level']}", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="<:cooking:1093765662964449311> Cooking",
                        value=f"{character.professions['cooking']['level']}", inline=True)

        embed.set_footer(text=f"character {index} out of {len(characters)}")
        index += 1
        embed_list.append(embed)

    return embed_list


def enable_button(button: discord.ui.Button, enabled: bool):
    if enabled:
        button.style = discord.ButtonStyle.green
        button.disabled = False
    else:
        button.style = discord.ButtonStyle.gray
        button.disabled = True


class Profile(discord.ui.View):
    def __init__(self, player: Player, original_interaction: discord.Interaction):
        super().__init__(timeout=40)
        self.rank, self.color = get_rank_info(player)
        self.original_interaction = original_interaction
        self.embeds = []
        self.index = 0
        self.embeds.append(profile_embed_constructor(player, self.rank, self.color))
        [self.embeds.append(character) for character in character_embed_constructor(player, self.color)]

    @discord.ui.button(label="◄", style=discord.ButtonStyle.gray, disabled=True)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(label="◉", style=discord.ButtonStyle.gray, disabled=True)
    async def profile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(label="►", style=discord.ButtonStyle.green)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user != self.original_interaction.user:
            await interaction.response.send_message("🛑 Only the author of the command can use the buttons!",
                                                    ephemeral=True)
            return False
        return True

    def update_buttons(self):
        if self.index == 0:
            # A LOT of redundancy, but it works sooooo :p
            enable_button(self.back_button, False)
            enable_button(self.profile_button, False)
            enable_button(self.next_button, True)
        elif self.index == len(self.embeds) - 1:
            enable_button(self.back_button, True)
            enable_button(self.profile_button, True)
            enable_button(self.next_button, False)
        else:
            enable_button(self.back_button, True)
            enable_button(self.profile_button, True)
            enable_button(self.next_button, True)

    async def on_timeout(self):
        self.back_button.disabled = True
        self.profile_button.disabled = True
        self.next_button.disabled = True
        self.back_button.style = discord.ButtonStyle.gray
        self.profile_button.style = discord.ButtonStyle.gray
        self.next_button.style = discord.ButtonStyle.gray
        await self.original_interaction.edit_original_response(view=self)
