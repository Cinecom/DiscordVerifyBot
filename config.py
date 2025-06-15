"""
Configuration settings for the Discord verification bot
"""

# Discord Channel and Role IDs
VERIFICATION_CHANNEL_ID = 1267765878183952396
OFFICER_ROLE_ID = 1234230977925222492

# Class Role IDs
CLASS_ROLES = {
    'Druid': 1234230977925222485,
    'Hunter': 1234230977925222484,
    'Mage': 1234230977925222483,
    'Priest': 1234230977899794489,
    'Rogue': 1234230977899794492,
    'Shaman': 1234230977899794491,
    'Warlock': 1234230977899794488,
    'Warrior': 1234230977899794490
}

# Gameplay Role IDs
GAMEPLAY_ROLES = {
    'DPS': 1234230977899794483,
    'Heal': 1234230977866498097,
    'Tank': 1234230977866498098
}

# Class Icons (custom server emojis)
CLASS_ICONS = {
    'Druid': '<:wowdruid:1236271638153003048>',
    'Hunter': '<:wowhunter:1236271639524540530>',
    'Mage': '<:wowmage:1236271641013784607>',
    'Priest': '<:wowpriest:1236271645174267984>',
    'Rogue': '<:wowrogue:1236271646554194012>',
    'Shaman': '<:wowshaman:1236271647976325130>',
    'Warlock': '<:wowwarlock:1236271650258026506>',
    'Warrior': '<:wowwarrior:1236271651658666064>'
}

# Role Icons (custom server emojis)
ROLE_ICONS = {
    'DPS': '<:wowdps:1236271995855831040>',
    'Heal': '<:wowhealer:1236271798962884660>',
    'Tank': '<:wowtank:1236271945784361070>'
}

# Bot Messages
WELCOME_MESSAGE = """
# **Welcome to the <ERROR> Discord Server!**

To gain access to all the member channels, please complete the verification below.

Click the button below to start your verification process.
"""

VERIFICATION_COMPLETE_MESSAGE = "An officer will soon grant you membership access to the server."
