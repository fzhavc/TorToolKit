

async def megadl(link, update_msg, user_msg):
    mega_client = await init_mega_client()

    path = os.path.join(os.getcwd(), "Downloads", str(time.time()).replace(".",""))
    pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
    dl_add_info = mega_client.addDl(link, path)
    
    dl_info = mega_client.getDownloadInfo(dl_add_info["gid"])
    
    dl_task = MegaDl(dl_add_info, dl_info, update_msg, mega_client)
    await dl_task.set_original_mess(user_msg)

    while True:
        dl_info = mega_client.getDownloadInfo(dl_add_info["gid"])
        if dl_info["state"] not in [constants.State.TYPE_STATE_CANCELED,constants.State.TYPE_STATE_FAILED]:
            if dl_info["state"] == constants.State.TYPE_STATE_COMPLETED:
                await dl_task.set_done()
                await update_msg.edit("Download Complete.")
                await asyncio.sleep(2)
                return dl_task
            try:
                await dl_task.refresh_info(dl_info)
                await dl_task.update_message()
                await asyncio.sleep(get_val("EDIT_SLEEP_SECS"))
            except Exception as e:
                torlog.info(e)
        else:
            if dl_info["state"] == constants.State.TYPE_STATE_CANCELED:
                await dl_task.set_inactive("Canceled by user.")
            else:
                await dl_task.set_inactive(dl_info["error_string"])
            return dl_task



