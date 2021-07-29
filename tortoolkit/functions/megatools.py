
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



