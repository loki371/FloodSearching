CURRENT_ID = 0

async def generate():
    global CURRENT_ID
    CURRENT_ID = CURRENT_ID + 1
    print("generateID: CURRENT_ID = ", CURRENT_ID)
    return CURRENT_ID