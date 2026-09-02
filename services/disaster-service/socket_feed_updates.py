from socket_app.socket_server import sio

async def card_update(report):
    await sio.emit('new_report', report)
   
async def card_del(report):
    await sio.emit('remove_report', report)
    
async def status_update(status):
    await sio.emit('status_update', status)
    
async def update_description(data):
    await sio.emit('update_description', data)