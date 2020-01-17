
cm = configManager.cm(dir = "default", file = "l_config.txt", verbose = True)
address = cm.loadData("apiMan", "address")
key = cm.loadData("apiMan", "key")
print("Loaded address {} and key {} from config.".format(address, key))


print(am.isReady())
print(am.getAPIconfig())
print(am.getLights())

cm = configManager.cm(dir = "default", file = "l_config.txt", verbose = True)
address = cm.loadData("apiMan", "address")
key = cm.loadData("apiMan", "key")
print("Loaded address {} and key {} from config.".format(address, key))


print(am.isReady())
print(am.getAPIconfig())
print(am.getLights())

lm = lightManager.lm(verbose = True)

test = cm.loadData(lm.CONFIG_NAME, lm.CONFIG_KEY)

lm.setConfig(test)

test2 = {
    "center": ["1", "2"],
    "left": ["3", "4"],
    "right": ["5"],
    "top": [],
    "bottom": []
}


print(lm.getConfig())

lm.addLightToGroup("3", "center")
print(lm.getConfig())

lm.addLightToGroup("3", "center")
print(lm.getConfig())

lm.addLightToGroup("1", "left")
print(lm.getConfig())

lm.removeLightFromGroup("1", "left")
print(lm.getConfig())

lm.removeLightFromGroup("1", "left")
print(lm.getConfig())


#cm.saveData(lm.CONFIG_NAME, lm.CONFIG_KEY, test)

lm.removeLightFromGroup("1", "center")
print(lm.getConfig())

print(lm.getLightsInGroup("center"))
