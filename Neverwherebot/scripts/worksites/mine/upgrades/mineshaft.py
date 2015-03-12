def on_install(worksite):
    worksite.depth_dug += 1
    worksite.save()
    return True