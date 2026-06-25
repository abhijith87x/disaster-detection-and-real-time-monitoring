from socket_app.socket_server import sio

async def card_update(report):
    print("reportttttttt socket",report)
    await sio.emit('new_report', report)
    print("socket emited")
   
async def card_del(report):
    await sio.emit('remove_report',report)
    print("del card emitted")