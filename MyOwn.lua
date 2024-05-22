local addonName = "MyOwn"
local appversion = 1.20240519

MyOwn = {}
MyOwn.SaveVars = {}
MyOwn.Helpers = {}

-- Initialize saved variables
function MyOwn.InitializeSavedVars()
    local defaults = {
        Name = "",
        FactionName = "",
        RaceName = "",
        ClassName = "",
        Level = 0,
        ChampionPoints = 0,
        isWerewolf = false,
        isVampire = false,
        Equipment = {},
        CharacterData = {
            activeAbilities = {},
            activeBuffs = {}},
    }
    MyOwn.SaveVars = ZO_SavedVars:NewCharacterIdSettings('MyOwnSavedVars', 1.11, nil, defaults, GetWorldName())
end

-- Function to save character data to saved variables
function MyOwn.SaveCharacterData()
    MyOwn.SaveVars.Name = GetUnitName("player")
    MyOwn.SaveVars.ClassName = string.gsub(GetUnitClass("player"), "%^.", "")
    MyOwn.SaveVars.RaceName = string.gsub(GetUnitRace("player"), "%^.", "")
    MyOwn.SaveVars.FactionName = MyOwn.Helpers.GetFactionName()
    MyOwn.SaveVars.Level = GetUnitLevel("player")
    MyOwn.SaveVars.ChampionPoints = GetPlayerChampionPointsEarned()
    MyOwn.SaveVars.isWerewolf = MyOwn.Helpers.IsWerewolf()
    MyOwn.SaveVars.isVampire = MyOwn.Helpers.IsVampire()
    MyOwn.SaveVars.Equipment = MyOwn.Helpers.GetEquippedItems()
    MyOwn.SaveVars.CharacterData.activeAbilities = MyOwn.Helpers.GetActiveAbilities()
    MyOwn.SaveVars.CharacterData.activeBuffs = MyOwn.Helpers.GetActiveBuffs()
end

-- Function to print the saved character data to the chat
function MyOwn.PrintCharacterDataToChat()
    if MyOwn.SaveVars.CharacterData then
        d("Character Name: " .. MyOwn.SaveVars.Name)
        d("Class: " .. MyOwn.SaveVars.ClassName)
        d("Race: " .. MyOwn.SaveVars.RaceName)
        d("Faction: " .. MyOwn.SaveVars.FactionName)
        d("Character Level: " .. tostring(MyOwn.SaveVars.Level))
        d("Champion Points: " .. tostring(MyOwn.SaveVars.ChampionPoints))
        d("Is Vampire: " .. tostring(MyOwn.SaveVars.isVampire))
        d("Is Werewolf: " .. tostring(MyOwn.SaveVars.isWerewolf))
        -- Print Equipment
        d("Equipped Items:")
        for _, item in ipairs(MyOwn.SaveVars.Equipment) do
            d("- " .. item.name .. " (ID: " .. item.slot .. ")")
        end
        -- Print active abilities
        d("Active Abilities:")
        for _, ability in ipairs(MyOwn.SaveVars.CharacterData.activeAbilities) do
            d("- " .. ability.name .. " (ID: " .. tostring(ability.id) .. ")")
        end
        -- Print active buffs
        d("Active Buffs:")
        for _, buff in ipairs(MyOwn.SaveVars.CharacterData.activeBuffs) do
            d("- " .. buff.name .. " (ID: " .. tostring(buff.id) .. ")")
        end
    else
        d("No character data found.")
    end
end
-- #################### Helper Functions #####################
MyOwn.Helpers.factionNames = {
    [ALLIANCE_ALDMERI_DOMINION] = "Aldmeri Dominion",
    [ALLIANCE_EBONHEART_PACT] = "Ebonheart Pact",
    [ALLIANCE_DAGGERFALL_COVENANT] = "Daggerfall Covenant"
}
MyOwn.Helpers.slotNames = {
    [EQUIP_SLOT_HEAD] = "Head",
    [EQUIP_SLOT_NECK] = "Neck",
    [EQUIP_SLOT_CHEST]= "Chest",
    [EQUIP_SLOT_SHOULDERS] = "Shoulders",
    [EQUIP_SLOT_MAIN_HAND] = "Main Hand",
    [EQUIP_SLOT_OFF_HAND] = "Off Hand",
    [EQUIP_SLOT_WAIST] = "Waist",
    [EQUIP_SLOT_LEGS] = "Legs",
    [EQUIP_SLOT_FEET]= "Feet",
    [EQUIP_SLOT_COSTUME] = "Costume",
    [EQUIP_SLOT_RING1] = "Ring 1",
    [EQUIP_SLOT_RING2] = "Ring 2",
    [EQUIP_SLOT_HAND] = "Gloves",
    [EQUIP_SLOT_BACKUP_MAIN] = "Backup Main Hand",
    [EQUIP_SLOT_BACKUP_OFF] = "Backup Off Hand",
}

function MyOwn.Helpers.GetFactionName()
    local alliance = GetUnitAlliance("player")
    return MyOwn.Helpers.factionNames[alliance] or "Unknown"
end

function MyOwn.Helpers.IsVampire()
    local vampireAbilityIds = {135397, 135398, 135399, 135400}
    for i = 1, GetNumBuffs("player") do
        local buffName, _, _, _, _, _, _, _, _, _, abilityId = GetUnitBuffInfo("player", i)
        if MyOwn.Helpers.Contains(vampireAbilityIds, abilityId) or string.find(buffName, "Vampir") then
            return true
        end
    end
    return false
end

function MyOwn.Helpers.IsWerewolf()
    local WolfAbilityIds = 35658
    for i = 1, GetNumBuffs("player") do
        local _, _, _, _, _, _, _, _, _, _, abilityId = GetUnitBuffInfo("player", i)
        if abilityId == WolfAbilityIds then
            return true
        end
    end
    return IsWerewolf()
end

function MyOwn.Helpers.Contains(table, value)
    for _, v in ipairs(table) do
        if v == value then
            return true
        end
    end
    return false
end

function MyOwn.Helpers.GetEquippedItems()
    local equippedItems = {}

    for equipSlot = EQUIP_SLOT_MIN_VALUE, EQUIP_SLOT_MAX_VALUE do
        local itemLink = GetItemLink(BAG_WORN, equipSlot)
        local itemName = ""
        local slotName = ""

        if itemLink ~= "" then
            itemName = string.gsub(GetItemLinkName(itemLink), "%^.", "")
            --slotName = MyOwn.Helpers.slotNames[equipSlot] or tostring(equipSlot)
            slotName = tostring(equipSlot)
            table.insert(equippedItems, {slot = slotName, name = itemName})
        end
    end

    return equippedItems
end

function MyOwn.Helpers.GetActiveAbilities()
    local abilities = {}
    -- Save active abilities from the active bar
    for i = 3, 8 do -- 1 and 2 are light and heavy attack
        local abilityId = GetSlotBoundId(i)
        local abilityName = GetAbilityName(abilityId)
        local formattedString = string.gsub(abilityName, "%^.", "")
        table.insert(abilities, {id = abilityId, name = formattedString})
    end

    return abilities
end

function MyOwn.Helpers.GetActiveBuffs()
    local buffs = {}
    -- Save active buffs
    for i = 1, GetNumBuffs("player") do
        local buffName, _, _, _, _, _, _, _, _, _, abilityId = GetUnitBuffInfo("player", i)
        local formattedString = string.gsub(buffName, "%^.", "")
        table.insert(buffs, {id = abilityId, name = formattedString})
    end

    return buffs
end
-- #################### Event handlers #######################
local function CollectAndPrint()
    MyOwn.SaveCharacterData()
    MyOwn.PrintCharacterDataToChat()
end

local function OnPlayerActivated(eventCode)
    MyOwn.SaveCharacterData()
end

local function OnPlayerDeactivated(eventCode)
    MyOwn.SaveCharacterData()
end

-- Initialize the addon
local function OnAddonLoaded(eventCode, addonNameLoaded)
    if addonNameLoaded == addonName then
        MyOwn.InitializeSavedVars()
        EVENT_MANAGER:RegisterForEvent(addonName, EVENT_PLAYER_ACTIVATED, OnPlayerActivated)
        EVENT_MANAGER:RegisterForEvent(addonName, EVENT_PLAYER_DEACTIVATED, OnPlayerDeactivated)
        SLASH_COMMANDS["/myown"] = CollectAndPrint
        EVENT_MANAGER:UnregisterForEvent(addonName, EVENT_ADD_ON_LOADED)
    end
end

EVENT_MANAGER:RegisterForEvent(addonName, EVENT_ADD_ON_LOADED, OnAddonLoaded)
