
            except Exception as e:
                torlog.info(e)
        else:
            if dl_info["state"] == constants.State.TYPE_STATE_CANCELED:
                await dl_task.set_inactive("Canceled by user.")
            else:
                await dl_task.set_inactive(dl_info["error_string"])
            return dl_task



