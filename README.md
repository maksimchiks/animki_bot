# Animki Bot

Highrise bot with animations, teleport, and clothing system.

## Commands

### Animations
- `1-270` - Send animation by number
- `0` - Stop animation
- `/dance` - Random dance for everyone
- `все X` - Send animation X to everyone

### Teleport
- `тп центр` - Teleport yourself to center
- `тп спавн` - Teleport yourself to spawn
- `тп ник центр` - Teleport someone to center
- `тп 5,0.25,10` - Teleport by coordinates

### Clothing
- `одежда` - Show clothing list
- `причёска 3` - Wear hairstyle #3
- `штаны 4` - Wear pants #4
- `одевать item_id` - Wear by item ID

### Other
- `позиция` - Show your coordinates
- `ping` - Check bot status

## Deployment to Railway

1. Push code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select this repository
5. Add environment variables:
   - `HIGHRISE_API_TOKEN` - Your Highrise API token
   - `HIGHRISE_ROOM_ID` - Your room ID
6. Deploy!

## Local Run

```bash
python bot.py
```

## Files

- `bot.py` - Main bot code
- `Procfile` - Railway deployment config
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version (3.11.9)
- `.env` - Environment variables (local)
