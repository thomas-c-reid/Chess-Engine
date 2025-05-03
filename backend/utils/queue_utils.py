import asyncio

async def peek_asyncio_queue(queue):
    items = []
    temp_queue = asyncio.Queue()
    
    # Extract items from the original queue, store them in a list, and put them in a temporary queue
    while not queue.empty():
        item = await queue.get()
        items.append(item)
        await temp_queue.put(item)
    
    # Restore the original queue contents
    while not temp_queue.empty():
        item = await temp_queue.get()
        await queue.put(item)
    
    return items