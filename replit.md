# Discord Verification Bot

## Overview

This is a Discord verification bot built with Python and discord.py that manages user onboarding through an interactive verification process. The bot guides new users through setting their character name, selecting their class, and choosing their gameplay role in what appears to be a gaming-focused Discord server.

## System Architecture

### Backend Architecture
- **Language**: Python 3.11
- **Framework**: discord.py (v2.5.2+)
- **Architecture Pattern**: Event-driven bot with persistent views
- **Configuration Management**: Environment variables with dotenv
- **Logging**: Built-in Python logging with file and console output

### Bot Structure
- **Main Bot Class**: `VerificationBot` extends `commands.Bot`
- **Intents**: Configured for message content, guilds, and members
- **Command System**: Uses `!` prefix (though primarily UI-driven)
- **Persistent Views**: UI components survive bot restarts

## Key Components

### Core Files
1. **main.py**: Entry point with async initialization and error handling
2. **bot.py**: Main bot class with event handlers and setup logic
3. **views.py**: Discord UI components (modals, buttons, dropdowns)
4. **config.py**: Static configuration including role IDs and messages

### UI Components
- **VerificationView**: Initial welcome interaction
- **ClassSelectionView**: Character class selection interface  
- **RoleSelectionView**: Gameplay role selection interface
- **CharacterNameModal**: Text input for character names

### Configuration System
- **Class Roles**: 8 predefined gaming classes (Druid, Hunter, Mage, etc.)
- **Gameplay Roles**: 3 role types (DPS, Heal, Tank)
- **Channel/Role IDs**: Hardcoded Discord IDs for server integration
- **Visual Elements**: Unicode icons for classes and roles

## Data Flow

### Verification Process
1. User joins server and sees welcome message in verification channel
2. User clicks verification button → Character name modal appears
3. User enters name → Nickname updated, class selection shown
4. User selects class → Class role assigned, gameplay role selection shown
5. User selects gameplay role → Final role assigned, verification complete

### State Management
- No persistent database - relies on Discord's role system
- Bot maintains references to channels and roles via IDs
- UI state managed through Discord's persistent view system

## External Dependencies

### Python Packages
- **discord.py**: Primary Discord API wrapper
- **python-dotenv**: Environment variable management
- **asyncio**: Built-in async runtime (Python standard library)

### Discord Permissions Required
- Read Messages
- Send Messages  
- Manage Nicknames
- Manage Roles
- Use Slash Commands (implied by intents)

## Deployment Strategy

### Environment Setup
- **Runtime**: Python 3.11 on Nix stable-24_05
- **Package Management**: UV lock file with pip fallback
- **Environment Variables**: Discord token and optional log level
- **Persistence**: Logs written to bot.log file

### Replit Configuration
- **Workflow**: Parallel execution with automatic dependency installation
- **Deployment**: Shell script runs pip install + python main.py
- **Development**: Interactive debugging with file logging

### Production Considerations
- Bot token security through environment variables
- Graceful shutdown handling with KeyboardInterrupt
- Error logging for troubleshooting
- No database backup needed (stateless design)

## Changelog
- June 15, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.