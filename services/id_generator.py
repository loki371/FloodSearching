CURRENT_ID = 0
MAX_GEN_ID = 500

async def generate():
    global CURRENT_ID, MAX_GEN_ID
    CURRENT_ID = (CURRENT_ID + 1) % MAX_GEN_ID
    print("generateID: CURRENT_ID = ", CURRENT_ID)
    return CURRENT_ID