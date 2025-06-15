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

# Class Icons (using common fantasy class symbols)
CLASS_ICONS = {
    'Druid': '🌿',
    'Hunter': '🏹',
    'Mage': '🔮',
    'Priest': '✨',
    'Rogue': '🗡️',
    'Shaman': '⚡',
    'Warlock': '🔥',
    'Warrior': '⚔️'
}

# Role Icons
ROLE_ICONS = {
    'DPS': '⚔️',
    'Heal': '💚',
    'Tank': '🛡️'
}

# Bot Messages
WELCOME_MESSAGE = """
**Welcome to the Discord Server!**

To gain access to all the member channels, please complete the verification below.

Click the button below to start your verification process.
"""

VERIFICATION_COMPLETE_MESSAGE = "🎉 **Verification Complete!** You now have access to all member channels. Welcome to the guild!"
